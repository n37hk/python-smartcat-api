################################################################################
# Smartcat API helper module
#
# Version: v1.0
# Date: October 26, 2020
# Author: Nooh A. Shaikh
# Support: nshaikh304@gmail.com
#
# Description:
# This module implement methods to Create Project, Delete Project, Get Project Id, Upload Doocument, Download Document, Get Document Id on top of GET, POST and DELETE requests
#
# Notes:
# > The Project created has pretranslation using MT enabled by default
################################################################################
import os
import requests
import base64
from configparser import ConfigParser

class Smartcat:
    def __init__(self, ):
        self.authorization_header = None
        self.debug = False


    _smartcat_url = {
        'project_create': 'https://smartcat.ai/api/integration/v1/project/create',
        'project_list': 'https://smartcat.ai/api/integration/v1/project/list',
        'project_general': 'https://smartcat.ai/api/integration/v1/project',
        'document_general': 'https://smartcat.ai/api/integration/v1/document',
        'document_upload': 'https://smartcat.ai/api/integration/v1/project/document',
        'document_download': 'https://smartcat.ai/api/integration/v1/document/export'
    }


    _config = ConfigParser()
    _config_file_path = '' # location of config file containing API credentials

    def set_debug(self, flag):
        ########################################################################
        # Enable or Disable debug
        # 
        # Args:
        # flag:
        #     > Datatype - boolean
        #     > set debug flag
        #
        # Return value:
        # > None
        ########################################################################
        self.debug = flag

    def save_to_config_file(self, config_filename, section, data):
        ########################################################################
        # Create or Update config file
        #
        # Args:
        # config_filename: 
        #     > Datatype - string
        #     > config filename to create or update
        # section: 
        #     > Datatype - string
        #     > section of config file
        # data:
        #     > Datatype - dictionary
        #     > data to be written
        #
        # Return value:
        # > Datatype - boolean
        # > Always True
        ########################################################################
        assert isinstance(config_filename, str), "'config_filename' should be of type 'str'"
        assert isinstance(section, str), "'section' should be of type 'str'"
        assert isinstance(data, dict), "'data' should be of type 'dict'"
        if not os.path.isfile(config_filename):
            self._config.write(open(config_filename,'w+'))
        else:
            self._config.read(config_filename)
        if section not in self._config.sections():
            self._config.add_section(section)
        self._config[section] = data
        with open(config_filename,'w+') as config_file:
            self._config.write(config_file)
        return True


###############################################################################
# API Configuration    

    def encode_authorization_data(self, api_login_id, api_key):
        ########################################################################
        # Encode API credentails to ASCII to prepare Authorization header
        #
        # Args: 
        # api_login_id:
        #     > Datatype - string
        #     > API logn ID
        # api_key:
        #     > Datatype - string
        #     > API Key
        #
        # Return Value:
        # > Datatype - string
        # > Encoded Authorization header
        ########################################################################
        assert isinstance(api_key, str), "'api_login_id' should be of type 'str'"
        assert isinstance(api_login_id, str), "'api_key' should be of type 'str'"
        auhtorization_data = api_login_id+':'+api_key
        return 'Basic '+base64.b64encode(auhtorization_data.encode('ascii')).decode('ascii')


    def save_api_credentials(self, api_login_id, api_key):
        ########################################################################
        #Save or Update API credentials to API config file
        #
        # Args: 
        # api_login_id:
        #     > Datatype - string
        #     > API logn ID
        # api_key:
        #     > Datatype - string
        #     > API Key
        #
        # Return Value:
        # > Datatype - boolean
        # > Always True
        ########################################################################
        self.save_to_config_file(self._config_file_path, 'API_CREDENTIALS', {'ID': api_login_id, 'API_KEY': api_key})
        return True
    

    def load_api_credentails(self):
        ########################################################################
        # Load saved API credentials from config file
        #
        # Args:
        #
        # Return value:
        # > Datatype - boolean
        # > True if loaded successfully else False
        ########################################################################
        try:
            with open(self._config_file_path) as f:
                pass
            self._config.read(self._config_file_path)
            api_login_id = self._config['API_CREDENTIALS']['ID']
            api_key = self._config['API_CREDENTIALS']['API_KEY']
            self.authorization_header = {'Authorization':self.encode_authorization_data(api_login_id, api_key)}
            return True
        except Exception as err:
            print(f'[Smartcat API:load_api_credentails]Exception: {err}')
            return False


################################################################################


################################################################################
# API Requests

    def get_request_smartcat(self, url, request_headers, request_data=None, request_query=None):
        ########################################################################
        # GET request to smartcat API
        #
        # Args:
        # url:
        #     > Datatype - string
        #     > url to make request to
        # request_headers:
        #     > Datatype - string
        #     > request headers - authorization header
        # request_data:
        #     > Datatype - string
        #     > request payload in JSON format
        # request_query:
        #     > Datatype - dictionary
        #     > query data to encode in url
        #
        # Return value:
        # > Datatype - requests.models.Response
        # > ressponse received
        ########################################################################
        assert isinstance(url, str), "'url' should be of type 'string'"
        assert isinstance(request_headers, dict), "'request_headers' should be of type 'dict'"
        form_data = {'':''}
        if (request_data != None):
            assert isinstance(request_data, str), "'request_data' should be of type 'string'"
            form_data = {'':('',request_data,'application/json')}
        if(request_query != None):
            assert isinstance(request_query, dict), "'request_query' should be of type 'dict'"
            q = ''
            for query in request_query.keys():
                if (query != list(request_query.keys())[-1]):
                    if isinstance(request_query[query], list):
                        for query_val in request_query[query]:
                            q += query+'='+query_val+'&'
                    else:
                        q += query+'='+request_query[query]+'&'
                else:
                    if isinstance(request_query[query], list):
                        for query_val in request_query[query]:
                            if(query_val != request_query[query][-1]):
                                q += query+'='+query_val+'&'
                            else:
                                q += query+'='+query_val
                    else:
                        q += query+'='+request_query[query]
            url = url+'?'+q
        if self.debug:
            print(f'[Smartcat API:GET]Request URL: {url}')
            print(f'[Smartcat API:GET]Request payload: {form_data}')
            print(f'[Smartcat API:GET]Request Query: {request_query}')
        # print(f'[GET]Request headers: {request_headers}')
        return requests.request('GET', url, files=form_data, headers=request_headers)


    def post_request_smartcat(self, url, request_headers, request_data=None, upload_file=None):
        ########################################################################
        # POST request to smartcat API
        #
        # Args:
        # url:
        #     > Datatype - string
        #     > url to make request to
        # request_headers:
        #     > Datatype - string
        #     > request headers - authorization header
        # request_data:
        #     > Datatype - string
        #     > request payload in JSON format
        # request_query:
        #     > Datatype - dictionary
        #     > query data to encode in url
        #
        # Return value:
        # > Datatype - requests.models.Response
        # > ressponse received
        ########################################################################
        assert isinstance(url, str), "'url' should be of type 'string'"
        if (request_data != None):
            assert isinstance(request_data, str), "'request_data' should be of type 'string'"
        assert isinstance(request_headers, dict), "'request_headers' should be of type 'dict'"
        if upload_file == None: 
            form_data = {'':('',request_data,'application/json')}
        else:
            if self.debug:
                print(f'[Smartcat API:POST]Upload Filename: {os.path.splitext(os.path.basename(upload_file))[0]}')
            form_data = {'':(os.path.basename(upload_file), open(upload_file, 'rb'),'application/octet-stream')}
        if self.debug:
            print(f'[Smartcat API:POST]Request URL: {url}')
            print(f'[Smartcat API:POST]Request payload: {form_data}')
            print(f'[Smartcat API:POST]Request headers: {request_headers}')
        return requests.request('POST', url, files=form_data, headers=request_headers)

    def delete_request_smartcat(self, url, request_headers, project_id=None, request_query=None):
        ########################################################################
        # DELETE request to smartcat API
        #
        # Args:
        # url:
        #     > Datatype - string
        #     > url to make request to
        # request_headers:
        #     > Datatype - string
        #     > request headers - authorization header
        # request_data:
        #     > Datatype - string
        #     > request payload in JSON format
        # request_query:
        #     > Datatype - dictionary
        #     > query data to encode in url
        #
        # Return value:
        # > Datatype - requests.models.Response
        # > ressponse received
        ########################################################################
        assert isinstance(url, str), "'url' should be of type 'string'"
        assert isinstance(request_headers, dict), "'request_headers' should be of type 'dict'"
        if (project_id != None):
            assert isinstance(project_id, str),"'project_id' should be of type 'string'"
            url = url+'/'+project_id
        if (request_query != None):
            assert isinstance(request_query, dict), "'request_query' should be of type 'dict'"
            q = ''
            for query in request_query.keys():
                if (query != list(request_query.keys())[-1]):
                    if isinstance(request_query[query], list):
                        for query_val in request_query[query]:
                            q += query+'='+query_val+'&'
                    else:
                        q += query+'='+request_query[query]+'&'
                else:
                    if isinstance(request_query[query], list):
                        for query_val in request_query[query]:
                            if(query_val != request_query[query][-1]):
                                q += query+'='+query_val+'&'
                            else:
                                q += query+'='+query_val
                    else:
                        q += query+'='+request_query[query]
            url = url+'?'+q
        if self.debug:
            print(f'[Smartcat API:DELETE]Request URL: {url}')
            print(f'[Smartcat API:DELETE]Request headers: {request_headers}')
        return requests.request('DELETE', url, files={'':''}, headers=request_headers)

    def make_response(self, response):
        ########################################################################
        # Reformat received reponse into dictionary

        # Args:
        # response:
        #     > Datatype - requests.models.Response
        #     > response of https resquest
        
        # Return value:
        # > Datatype - dictionary
        # > dictionary of response code and content
        ########################################################################
        try:
            return {'response_code':response.status_code, 'response':response.json()}
        except Exception as err:
            print(f'[Smartcat API:make_response]Exception: {err}')
            return {'response_code':response.status_code, 'response':''}


################################################################################


################################################################################
# API Operation Methods

    def create_project(self, project_name, source_language, target_languages, pretranslate=True):
        ########################################################################
        # Create project in Smartcat workspace
        #
        # Args:
        # project_name:
        #     > Datatype - string
        #     > name of the projct to be createtd
        # source_language:
        #     > Datatype - string
        #     > language of content of files in the project
        # target_languages:
        #     > Datatype - list
        #     > list of languages, the files are to be translated
        # pretranslate:
        #     > Datatype - boolean
        #     > Enable or disable pretranslation for a project
        #
        # Return value:
        # > Datatype - dictionary
        # > dictionary of reponse code and response content containing project id and other information
        ########################################################################
        assert isinstance(project_name, str), "'project_name' should be of type 'string'"
        assert isinstance(source_language, str), "'source_language' should be of type 'string'"
        assert isinstance(target_languages, list), "'target_languages' should be of type 'list'"
        assert isinstance(pretranslate, bool), "'pretranslate' should be of type 'boolean'"
        enable_pretranslation = 'true'
        if pretranslate == False:
            enable_pretranslation = 'false'
        target_languages_str = '"'
        for language in target_languages:
            if target_languages[-1] == language:
                target_languages_str = target_languages_str+language+'"'
            else:
                target_languages_str = target_languages_str+language+'","'
        payload = f'{{"name":"{project_name}","sourceLanguage": "{source_language}","targetLanguages": [{target_languages_str}],"assignToVendor": false,"useMT": {enable_pretranslation},"pretranslate": {enable_pretranslation},"autoPropagateRepetitions": true}}'
        if self.debug:
            print(f'[Smartcat API:create_project]Request payload: {payload}')
        return self.make_response(self.post_request_smartcat(self._smartcat_url['project_create'], self.authorization_header, request_data=payload))


    def get_project_id(self, project_name):
        ########################################################################
        # Get project Id of the project
        #
        # Args:
        # project_name:
        #     > Datatype - string
        #     > name of the project whose id is to be fetched
        #
        # Return value:
        # > Datatype - string
        # > project id of the given project name
        ########################################################################
        assert isinstance(project_name, str), "'project_name' should be of type 'string'"
        if self.debug:
            print(f'[Smartcat API:get_project_id]Project Name: {project_name}')
        return self.get_request_smartcat(self._smartcat_url['project_list'], self.authorization_header, request_query={'projectName':project_name}).json()[0]['id'] 



    def delete_project(self, project_name):
        ########################################################################
        # Delete project
        #
        # Args:
        # project_name:
        #     > Datatype - string
        #     > name of the projct to be deleted
        #
        # Return value:
        # > Datatype - boolean
        # > True if project deleted else False
        ########################################################################
        assert isinstance(project_name, str),"'project_id' should be of type 'string'"
        project_id = self.get_project_id(project_name)
        if self.debug:
            print(f'[Smartcat API:delete_project]Project Name: {project_name}')
            print(f'[Smartcat API:delete_project]Project Id: {project_id}')
        resp = self.delete_request_smartcat(self._smartcat_url['project_general'], self.authorization_header, project_id=project_id)
        if (resp.status_code == 204):
            return True
        else:
            return False


    def upload_document(self, project_name, file_path):
        ########################################################################
        # Upload file to a project
        # 
        # Args:
        # project_name:
        #   > Datatype - string
        #   > name of the eproject to which the file is to be uploaded
        #
        # Return value:
        # > Datatype - boolean
        # > True if file uploaded else False
        ########################################################################
        assert isinstance(file_path, str), "'file_path' should be of type 'str'"
        try:
            with open(file_path, 'r') as file:
                pass
            assert isinstance(project_name, str), "'project_name' should be of type 'str'"
            project_id = self.get_project_id(project_name)
            url = self._smartcat_url['document_upload']+'?projectId='+project_id
            if self.debug:
                print(f'[Smartcat API:upload_document]Project Id: {project_id}')
                print(f'[Smartcat API:upload_document]Request URL: {url}')
            resp = self.post_request_smartcat(url, self.authorization_header, upload_file=file_path)
            if (resp.status_code == 200):
                return True
            else:
                return False
        except Exception as err:
            print(f'[Smartcat API:upload_document]Exception: {err}')
            return False


    def get_document_id(self, project_name, document_names):
        ########################################################################
        # Get document Id of documents
        #
        # Args:
        # project_name:
        #     > Datatype - string
        #     > name of the project whose id is to be fetched
        # document_names:
        #     > Datatyepe - list
        #     > list of documents whose id is to be fetched
        #
        # Return value:
        # > Datatype - dictionary
        # > dictionary of document ids with document name as key and list of ids of document. If a project has more than one target languages, multiple copies of the same document is created for each target language with separate id in the format documentid_languageid
        ########################################################################
        assert isinstance(project_name, str), "'project_name' should be of type 'string'"
        assert isinstance(document_names, list), "'document_name' should be of type 'list'"
        if self.debug:
            print(f'[Smartcat API:get_document_id]Project Name: {project_name}')
        project_documents = self.get_request_smartcat(self._smartcat_url['project_list'], self.authorization_header, request_query={'projectName':project_name}).json()[0]['documents']
        # print(f'[Get Document ID]Prjoct Documents: {project_documents}')
        doc_ids = {}
        for doc_name in document_names:
            document_name = os.path.splitext(os.path.basename(doc_name))[0]
            if self.debug:
                print(f'[Smartcat API:get_document_id]Document Name: {document_name}')
            doc_id = []
            for doc in project_documents:
                if (doc['name'] == document_name):
                    doc_id.append(doc['id'])
            doc_ids[document_name] = doc_id
        if self.debug:
            print(f'[Smartcat API:get_document_id]Document ID: {doc_ids}')
        return doc_ids
    
    def get_document_word_count(self, project_name, document_names):
        ########################################################################
        # Get document word count
        #
        # Args:
        # project_name:
        #     > Datatype - string
        #     > name of the project whose id is to be fetched
        # document_names:
        #     > Datatyepe - list
        #     > list of documents whose id is to be fetched
        #
        # Return value:
        # > Datatype - dictionary
        # > dictionary of word count with document name as key and list of status and word count of document.
        ########################################################################
        word_count = {}
        doc_ids = self.get_document_id(project_name, document_names)
        for doc in doc_ids.keys():
            received_response = self.make_response(self.get_request_smartcat(self._smartcat_url['document_general']+'/statistics', self.authorization_header, request_query={'documentId': doc_ids[doc]}))
            if received_response['response_code'] == 200:
                word_count[doc] = [True, received_response['response']['statistics'][0]['words']]
            else:
                word_count[doc] = [False, 'Build statistics in progress']
        return word_count


    def delete_document(self, project_name, document_names):
        ########################################################################
        # Delete document(s)
        #
        # Args:
        # project_name:
        #     > Datatype - string
        #     > name of the project from which document(s) is to be deleted
        # document_names:
        #     > Datatype - list
        #     > list of documents to be deleted
        #
        # Return value:
        # > Datatype - boolean
        # > True if document(s) deleted else False
        ########################################################################
        assert isinstance(document_names, list), "'document_names' should be of type 'list'"
        doc_ids = self.get_document_id(project_name, document_names)
        if self.debug:
            print(f'[Smartcat API:delete_document]Document(s): {doc_ids}')
        delete_doc_ids = []
        for doc in doc_ids.keys():
            for Id in doc_ids[doc]:
                delete_doc_ids.append(Id)
        query = {'documentIds': delete_doc_ids}
        if self.debug:
            print(f'[Smartcat API:delete_document]Document Id(s): {query}')
        resp = self.delete_request_smartcat(self._smartcat_url['document_general'], self.authorization_header, request_query=query)
        if (resp.status_code == 204):
            return True
        else:
            return False


    def check_doc_pretranslation_status(self, project_name, document_names):
        ########################################################################
        # Check Pretranslation status of document(s)
        #
        # Args:
        # project_name:
        #     > Datatype - string
        #     > name of the project from which document(s) is to be deleted
        # document_names:
        #     > Datatype - list
        #     > list of documents to be deleted
        #
        # Return value:
        # > Datatype - dictionary
        # > dictionary of status with document name as key and boolean status as value
        ########################################################################
        assert isinstance(project_name, str), "'project_name' should be of type 'string'"
        assert isinstance(document_names, list), "'document_names' should be of type 'list'"
        if self.debug:
            print(f'[Smartcat API:check_doc_pretranslation_status]Project Name: {project_name}')
        project_documents = self.get_request_smartcat(self._smartcat_url['project_list'], self.authorization_header, request_query={'projectName':project_name}).json()[0]['documents']
        doc_status = {}
        for doc_name in document_names:
            document_name = os.path.splitext(os.path.basename(doc_name))[0]
            if self.debug:
                print(f'[Smartcat API:check_doc_pretranslation_status]Document Name: {document_name}')
            for doc in project_documents:
                if (doc['name'] == document_name):
                    doc_status[document_name] = doc["pretranslateCompleted"]
        if self.debug:
            print(f'[Smartcat API:check_doc_pretranslation_status]Document Status: {doc_status}')
        return doc_status


    def get_doc_task_id(self, document_id):
        ########################################################################
        # Get task id for document download. Each task id is for one time use only
        #
        # Args:
        # document_id:
        #     > Datatype - string
        #     > id of document to be downloaded
        #
        # Return value:
        # > Datatype - list(boolean, string)
        # > task id
        ########################################################################
        assert isinstance(document_id, str), "'document_id' should be of type 'string'"
        url = self._smartcat_url['document_download']+'?documentIds='+document_id
        resp = self.make_response(self.post_request_smartcat(url, self.authorization_header))
        if (resp['response_code'] == 200):
            return resp['response']['id']
        else:
            return resp['response']


    def download_document(self, project_name, document_name, document_save_as):
        ########################################################################
        # Download translated document
        #
        # Args:
        # project_name:
        #     > Datatype - string
        #     > name of the project from which document(s) is to be downloaded
        # document_name:
        #     > Datatype - string
        #     > name of the document
        # document_save_as:
        #     > Datatype - string
        #     > filename with path to save documnet as
        #
        # Return value:
        # > Datatype - boolean
        # > True if document downloaded else False
        ########################################################################
        assert isinstance(project_name, str), "'project_name' should be of type 'string'"
        assert isinstance(document_name, str), "'document_name' should be of type 'string'"
        assert isinstance(document_save_as, str), "'document_save_as' should be of type 'string'"
        if self.debug:
            print(f'[Smartcat API:download_document]Project Name: {project_name}')
            print(f'[Smartcat API:download_document]Document Name: {document_name}')
            print(f'[Smartcat API:download_document]Save Document: {document_save_as}')
        doc_name = os.path.splitext(os.path.basename(document_name))[0]
        doc_id = self.get_document_id(project_name, [document_name])[doc_name][0]
        task_id = self.get_doc_task_id(doc_id)
        if task_id != '':
            url = self._smartcat_url['document_download']+'/'+task_id
            file_content = self.get_request_smartcat(url, self.authorization_header)._content
            if self.debug:
                print(f'[Smartcat API:download_document]Response: {file_content}')
            with open(document_save_as, 'wb+') as f:
                f.write(file_content)
            return True
        else:
            return False


################################################################################