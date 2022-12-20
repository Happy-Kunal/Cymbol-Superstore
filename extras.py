from fastapi import Path, Query, Body


Query_Tags = Query(alias="tag", max_length=50)