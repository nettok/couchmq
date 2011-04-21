function(doc, req) {
    if (doc.state == req.query.state) {
        return true;
    }
    return false;
}
