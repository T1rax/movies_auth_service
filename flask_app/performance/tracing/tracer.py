import functools
from flask import request, current_app
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider    
from opentelemetry.sdk.resources import Resource    
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.jaeger.thrift import JaegerExporter


tracer = trace.get_tracer(__name__)


def read_x_request_id_header(app) -> None:

    @app.before_request
    def read_x_request_id():
        request_id = request.headers.get('X-Request-Id')
        if not request_id:
            current_app.logger.info('No request ID')
            raise RuntimeError('request id is required') 
        
        span = tracer.start_span('set_request_id')
        span.set_attribute('http.request_id', request_id)
        span.end() 
        

def configure_tracer(app) -> None:
    read_x_request_id_header(app)

    resource = Resource(attributes={
        "service.name": "auth_api"
    })

    trace.set_tracer_provider(TracerProvider(resource=resource))
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name='jaeger',
                agent_port=6831,
            )
        )
    )
    # Чтобы видеть трейсы в консоли
    # trace.get_tracer_provider().add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))

    FlaskInstrumentor().instrument_app(app) 


def trace_it(input_function):
   @functools.wraps(input_function)
   def trace_wrapper(*args, **kwargs):
        with tracer.start_as_current_span(input_function.__name__):
            return_value = input_function(*args, **kwargs)
        return return_value
   return trace_wrapper