% prepara el repositorio para su despliegue. 
release: sh -c 'cd decide && python manage.py migrate'
% genera los archivos estáticos para lanzar decide
generatestatics: sh -c 'cd decide && python manage.py collectstatic'
% especifica el comando para lanzar Decide
web: sh -c 'cd decide && gunicorn decide.wsgi --log-file -' 