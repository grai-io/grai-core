from locust import HttpUser, between, task

# headers = {"Authorization": "Api-Key kIgnpnGR.2y4QfYc1ea966nFYyjCUPX2FotcBfMxp"} # localhost
headers = {"Authorization": "Api-Key mrQ0XbZu.nG0znSOEnb0KoOluICxA7pcT4Oq3EfiB"}  # cloud


class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    @task
    def health(self):
        self.client.get("/health/")

    @task
    def admin(self):
        self.client.get("/admin/")

    @task
    def admin_with_headers(self):
        self.client.get("/admin/", headers=headers)

    @task
    def nodes(self):
        self.client.get("/api/v1/lineage/nodes/", headers=headers)

    @task
    def edges(self):
        self.client.get("/api/v1/lineage/edges/", headers=headers)


# from locust import HttpLocust, TaskSet, task


# class UserActions(TaskSet):


#     # def on_start(self):
#     #     self.login()


#     # def login(self):
#     #     # login to the application
#     #     response = self.client.get('/accounts/login/')
#     #     csrftoken = response.cookies['csrftoken']
#     #     self.client.post('/accounts/login/',
#     #                      {'username': 'username', 'password': 'password'},
#     #                      headers={'X-CSRFToken': csrftoken})


#

#     @task(1)
#     def admin(self):
#         self.client.get('/admin/', headers=self.headers)


#     # for i in range(4):
#     #     @task(2)
#     #     def first_page(self):
#     #         self.client.get('/list_page/')


#     # @task(3)
#     # def get_second_page(self):
#     #     self.client.('/create_page/', {'name': 'first_obj'}, headers={'X-CSRFToken': csrftoken})


#     # @task(4)
#     # def add_advertiser_api(self):
#     #     auth_response = self.client.post('/auth/login/', {'username': 'suser', 'password': 'asdf1234'})
#     #     auth_token = json.loads(auth_response.text)['token']
#     #     jwt_auth_token = 'jwt '+auth_token
#     #     now = datetime.datetime.now()

#     #     current_datetime_string = now.strftime("%B %d, %Y")
#     #     adv_name = 'locust_adv'
#     #     data = {'name', current_datetime_string}
#     #     adv_api_response = requests.post('http://127.0.0.1:8000/api/advertiser/', data, headers={'Authorization': jwt_auth_token})


# class ApplicationUser(HttpLocust):
#     task_set = UserActions()
#     min_wait = 0
#     max_wait = 0
