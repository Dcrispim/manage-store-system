def prefixID(ID, prefix):
    lenP = len(prefix)
    new_id = str(ID).replace(str(prefix),'')
    if new_id != str(ID):
        if len(new_id)>0:
            return new_id
    else:
        return False
