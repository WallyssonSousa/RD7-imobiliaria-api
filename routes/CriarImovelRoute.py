from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import os
from datetime import timedelta
from flask_jwt_extended import JWTManager