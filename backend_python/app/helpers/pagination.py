def paginate_query(query, limit, offset):
    return query.limit(limit).offset(offset)
