from ssgateway.models import DBSession
from pyramid.httpexceptions import HTTPNotFound


def process_form(request, form, post_validate_fn):
    if request.method == 'POST' and form.validate():
        return post_validate_fn(form)
    else:
        return {'form': form}


def get_object_or_404(kls, id):
    """
    Function to find an object from the database by its id.
    Args: class for query the database for
          id of the object you want.
    Returns:
       The Object if it is found in the database.
       Or a 404 is the query resultls in None

    """
    if id is None:
        raise HTTPNotFound('No id provided')
    session = DBSession()
    obj = session.query(kls).get(id)
    if obj is None:
        raise HTTPNotFound()
    else:
        return obj
