class CorsMiddleware(object):
    def process_response(self, req, resp):
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Headers"] =  "Content-Type"
        return response
