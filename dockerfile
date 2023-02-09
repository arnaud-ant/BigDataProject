FROM public.ecr.aws/lambda/python:3.9
ENV SKLEARN_ALLOW_DEPRECATED_SKLEARN_PACKAGE_INSTALL True
COPY . .
RUN pip3 install -r requirements.txt
