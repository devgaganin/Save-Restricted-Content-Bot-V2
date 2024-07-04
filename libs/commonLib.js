function getNameFor(member){
  let haveAnyNames = member.username||member.first_name||member.last_name;
  if(!haveAnyNames){ return ""}

  if(member.username){
    return "@" + member.username
  }

  return member.first_name ? member.first_name : member.last_name
}

function getLinkFor(member, parse_mode){
  let name = getNameFor(member);
  if(name==""){
    name = member.telegramid;
  }

  if(!parse_mode){
    return "[" + name + "](tg://user?id=" + member.telegramid + ")";
  }

  return "<a href=\"tg://user?id=" + member.telegramid + "\">" + name + "</a>";
}

publish({
    getNameFor: getNameFor,
    getLinkFor: getLinkFor
})

