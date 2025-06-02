from flask import Flask
from flask_cors import CORS

# 라우트 모듈 임포트
from Flask_func_APP.flask_ranking import ranking_bp
from Flask_func_APP.flask_report import report_bp
from Flask_func_APP.flask_current_umbrella import  current_umbrella_bp
from Flask_func_APP.flask_user_info import user_info_bp
from Flask_func_APP.flask_rental_log import rental_log_bp
from Flask_func_APP.flask_login import login_bp
from Flask_func_APP.flask_weather import weather_bp
from Flask_func_APP.flask_report_image import image_bp
# from Flask_func_APP.flask_umbrella_location import location_store_bp, location_find_bp
from Flask_func_APP.flask_get_umbrella_info import get_umbrella_info_bp,get_umbrella_place_bp,store_umbrella_place_bp


app = Flask(__name__)
CORS(app)

# 필요한 다른 모듈도 여기서 추가
# 라우트 등록
# 다른 Blueprint도 등록
app.register_blueprint(ranking_bp)
app.register_blueprint(report_bp)
app.register_blueprint(current_umbrella_bp)
app.register_blueprint(rental_log_bp)
app.register_blueprint(user_info_bp)
app.register_blueprint(login_bp)
app.register_blueprint(weather_bp)
app.register_blueprint(image_bp)
# app.register_blueprint(location_store_bp)
# app.register_blueprint(location_find_bp)
app.register_blueprint(get_umbrella_info_bp)
app.register_blueprint(get_umbrella_place_bp)
app.register_blueprint(store_umbrella_place_bp)

if __name__ == '__main__':
    print(app.url_map)
    app.run(host='0.0.0.0', port=5000, debug=True)
