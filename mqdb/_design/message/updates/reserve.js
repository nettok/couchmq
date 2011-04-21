function(doc, req) {
    if (doc.state == "available") {
        doc.state = "reserved";
        return [doc, "ok"];
    }
    return [null, "unavailable"];
}
