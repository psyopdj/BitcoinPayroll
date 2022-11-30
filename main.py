from setup import app
from src.api.route.employee import employee_api
from src.api.route.shift import shift_api

app.register_blueprint(employee_api)
app.register_blueprint(shift_api)

if __name__ == '__main__':
    app.run()
