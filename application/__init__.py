from flask import Flask, request
from flask_restful import Api
from database.database import Database
from core_lib.utils.global_config import Config
from flask_oidc import OpenIDConnect                                            
oidc = OpenIDConnect()

from resources.smart_tricks import askfor, DictObj
def get_userinfo():
    userinfo = askfor.get('api/system/user_info', headers=request.headers).json()
    user = DictObj(userinfo)
    return user

def create_app():
	app = Flask(__name__)
	app.config.from_object('config')
	oidc.init_app(app)

	# Add API resources
	from api.ticket_api import (CreateTicketAPI, 
								DeleteTicketAPI,
	                            UpdateTicketAPI,
	                            GetTicketAPI,
	                            GetEditableTicketAPI,
	                            CreateRelValsForTicketAPI,
	                            GetWorkflowsOfCreatedRelValsAPI,
	                            GetRunTheMatrixOfTicketAPI)
	from api.relval_api import (CreateRelValAPI,
                            DeleteRelValAPI,
                            UpdateRelValAPI,
                            GetRelValAPI,
                            GetEditableRelValAPI,
                            GetCMSDriverAPI,
                            GetConfigUploadAPI,
                            GetRelValJobDictAPI,
                            GetDefaultRelValStepAPI,
                            RelValNextStatus,
                            RelValPreviousStatus,
                            UpdateRelValWorkflowsAPI)
	from api.system_api import UserInfoAPI
	from api.search_api import SearchAPI, SuggestionsAPI, WildSearchAPI

	api = Api(app)
	api.add_resource(CreateTicketAPI, '/api/tickets/create')
	api.add_resource(DeleteTicketAPI, '/api/tickets/delete')
	api.add_resource(UpdateTicketAPI, '/api/tickets/update')
	api.add_resource(GetTicketAPI, '/api/tickets/get/<string:prepid>')
	api.add_resource(GetEditableTicketAPI, 
					 '/api/tickets/get_editable', 
					 '/api/tickets/get_editable/<string:prepid>')
	api.add_resource(CreateRelValsForTicketAPI, '/api/tickets/create_relvals')
	api.add_resource(GetWorkflowsOfCreatedRelValsAPI,
                 '/api/tickets/relvals_workflows/<string:prepid>')
	api.add_resource(GetRunTheMatrixOfTicketAPI, '/api/tickets/run_the_matrix/<string:prepid>')

	api.add_resource(CreateRelValAPI, '/api/relvals/create')
	api.add_resource(DeleteRelValAPI, '/api/relvals/delete')
	api.add_resource(UpdateRelValAPI, '/api/relvals/update')
	api.add_resource(GetRelValAPI, '/api/relvals/get/<string:prepid>')
	api.add_resource(GetEditableRelValAPI,
	                 '/api/relvals/get_editable',
	                 '/api/relvals/get_editable/<string:prepid>')
	api.add_resource(GetCMSDriverAPI, '/api/relvals/get_cmsdriver/<string:prepid>')
	api.add_resource(GetConfigUploadAPI, '/api/relvals/get_config_upload/<string:prepid>')
	api.add_resource(GetRelValJobDictAPI, '/api/relvals/get_dict/<string:prepid>')
	api.add_resource(GetDefaultRelValStepAPI, '/api/relvals/get_default_step')
	api.add_resource(RelValNextStatus, '/api/relvals/next_status')
	api.add_resource(RelValPreviousStatus, '/api/relvals/previous_status')
	api.add_resource(UpdateRelValWorkflowsAPI, '/api/relvals/update_workflows')


	api.add_resource(UserInfoAPI, '/api/system/user_info')
	api.add_resource(SearchAPI, '/api/search')
	api.add_resource(SuggestionsAPI, '/api/suggestions')
	api.add_resource(WildSearchAPI, '/api/wild_search')

	# Register Blueprints
	from .relvals.views import relval_blueprint
	from .home_view import home_blueprint
	from .tickets.view import ticket_blueprint

	app.register_blueprint(relval_blueprint, url_prefix='/')
	app.register_blueprint(home_blueprint, url_prefix='/')
	app.register_blueprint(ticket_blueprint, url_prefix='/')


	# To avoid trailing slashes at the end of the url
	app.url_map.strict_slashes = False
	@app.before_request
	def clear_trailing():
	    from flask import redirect, request
	    rp = request.path 
	    if rp != '/' and rp.endswith('/'):
	        return redirect(rp[:-1])

	config = Config.load('config.cfg', 'prod')
	# Init database connection
	Database.set_database_name('relval')
	Database.add_search_rename('tickets', 'created_on', 'history.0.time')
	Database.add_search_rename('tickets', 'created_by', 'history.0.user')
	Database.add_search_rename('tickets', 'workflows', 'workflow_ids<float>')
	Database.add_search_rename('relvals', 'created_on', 'history.0.time')
	Database.add_search_rename('relvals', 'created_by', 'history.0.user')
	Database.add_search_rename('relvals', 'workflows', 'workflows.name')
	Database.add_search_rename('relvals', 'workflow', 'workflows.name')
	Database.add_search_rename('relvals', 'output_dataset', 'output_datasets')
	return app
