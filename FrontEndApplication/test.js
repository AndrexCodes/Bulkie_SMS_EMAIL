var datetime = new Date()
year = `${datetime.getFullYear()}`
month = `${datetime.getMonth()+1}`
date = `${datetime.getDate()}`
hour = `${datetime.getHours()}`
minute = `${datetime.getMinutes()}`
datetime = `${year}-${month}-${date} ${hour}:${minute}`
console.log(datetime)