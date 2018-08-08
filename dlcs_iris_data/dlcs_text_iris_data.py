from iris_data.iris_data_s3 import IrisSessionData
from iris_data.exceptions import IrisDataError

class TextPipelineIrisData:

    def __init__(self):

        self.session_data = IrisSessionData()

    def get_all_data(self, session_id):

        data = self.session_data.get_json_data(session_id)
        return self.session_data.expand_json_obj(data)

    def get_manifest_data(self, session_id, service):

        data = self.session_data.get_json_data(session_id)
        data = self.session_data.expand_json_obj(data)
        if "services" not in data:
            raise IrisDataError("services element not present")
        if service in data['services']:
            return data["services"][service]
        return {}

    def get_canvas_data(self, session_id, service, canvas_id):

        data = self.session_data.get_json_data(session_id)
        data = self.session_data.expand_json_obj(data)
        combined_data = {}
        if "services" not in data:
            raise IrisDataError("services element not present")
        if service in data['services']:
            combined_data["manifest"] = data["services"][service]
        if "canvases" in data and canvas_id in data["canvases"]:
            canvas_data = data["canvases"][canvas_id]
            if "services" in canvas_data and service in canvas_data["services"]:
                combined_data["canvas"] = canvas_data["services"][service]
        return combined_data

    # pass throughs

    def get_unexpanded_data(self, session_id):

        return self.session_data.get_json_data(session_id)

    def store_data(self, session_id, json_data):

        self.session_data.store_json_data(session_id, json_data)

    def store_shared_data(self, shared_id, json_data):

        self.session_data.store_shared_json_data(shared_id, json_data)
