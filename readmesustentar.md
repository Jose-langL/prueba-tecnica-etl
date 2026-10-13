meter credenciales de postgres en terminal 
psql -h localhost -p 5434 -U etl_user -d electoral_db 

comando para cambiar el metodo de busqueda y hacer que busque por el schema.
SET search_path TO electoral;

