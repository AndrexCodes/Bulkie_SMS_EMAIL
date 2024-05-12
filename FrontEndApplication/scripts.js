const create_account_screen = document.getElementById("create_account_screen")
const sign_in_account = document.getElementById("sign_in_account")
const dashboard_screen = document.getElementById("dashboard_screen")
const acc_groups = document.getElementById("acc_groups")
const sms_email_send = document.getElementById("sms_email_send")
const group_contacts = document.getElementById("group_contacts")
const add_contact = document.getElementById("add_contact")
const account_screen = document.getElementById("account_screen")
const loading_screen = document.getElementById("loading_screen")
const alert_box = document.getElementById("alert_box")
const history_screen = document.getElementById("history_screen")
const splash_screen = document.getElementById("splash_screen")
const verification_screen = document.getElementById("verification_screen")
const all_screens = [create_account_screen, sign_in_account, dashboard_screen, acc_groups, sms_email_send, group_contacts, add_contact, account_screen, history_screen, splash_screen, verification_screen]

// const home_url = "http://127.0.0.1:5000"
const home_url = "https://ionextechsolutions.com/bulkies"
const new_born_key = "ZITD0JL2LCZMJVQENIFH2Y7VXZ5JMLGWMAHQ9K7STV8FIBW9PARNFKWXL6VMFRK24IBJ5YJUKLYS3NBRKO8GCG67M5BF4RKMT8AYKW9B9I7W5YBLW1V942O16NVKDBLWPGG7LQKQEEAWLWR9J593RH2TR88EY91OJ7NUVF58UGGKGFKVVY9P01I5WYF4NO42TXNB93Q8AU0EHN3I6GGOHDO9MVEJXIGNXPZJJNAWTJB649JLLEHX5B1X5NKNWYXL2O5E9GS0HR4P94US4FNVOFZHOQZZY0KB2KYFK37P2B3PEKV1DLVH62ZBUS2URLAAOCVDW6CIHH5F9LTNQJ00JT7VR9KPHHTYAX5NTL0K6H6ZTH480XL8NPJZ4V54D88BM0M3USK4QMZV9Q7XOAH55YCIAZWNB7OPRJLW1LEFGP13ZYQ2WF5IR3SS2IR44E7MLXKN6U1H1IHACYCGG09EJG67DJFC6B4GFKNRKAQGX00X338P6JGGYU2Q38OBR9IJBWD6R8LK5KLDI6PKYHHQ3RZ6UUVV0VVMYECNZ2CP3SUL8C7TZIF4NPLR24CAOBLLJGR0DC6VLPD3LBDPAUU5TDVNBYJPWAGW69SK2YZVCWZ49R135DVJLKNOSVLK0L0PHT8KKHWSULOQJYD1VKFAILFF1CPT3UJZD5BV23DAOIXVU1O220KR5P1QE6GWYLUQ1M1CF3ZHIKXR0986WODXYMHNQGGGYESNFZBAIS2N8QH6HOBBOEW2D2V3RQ60LIGITXCX6CUM38VMN45UGHI5T691R478H24QMZCLW5H5A25GQUWVNDX6C4VEBNC9KX00UGREHHJN5Q7VYHETVMYW21OBJQATUKWI9YAIAX9EUCBIS94WYC75E160RE4S75OFJ70JBUJ67C2WINSJXGSJH1G65EQYJ208UYV8PUYEN5X8SC3M98XNEZOQDOIE0QTKNXC2NOLOBZRMILR1TOTEX7G3BEV3A722Y8EZSHOS"
var sendToCommunities = []

function splashdelay(){
    console.log("splash is on")
    screenManager(9)
    setTimeout(()=>{
        AppInit()
    }, 7000)
}

function killAllScreens(){
    all_screens.forEach(screen=>{
        screen.style.display = "none"
    })
}

function screenManager(screen_no){
    killAllScreens()
    console.log(screen_no)
    non_flex_group = [5]
    if(screen_no === 5 || screen_no === 3 || screen_no === 4 || screen_no === 7 || screen_no === 8 || screen_no === 10){
        all_screens[screen_no].style.display = "block"
    }else{
        all_screens[screen_no].style.display = "flex"
    }
}

function AppInit(){
    var app_id = localStorage.getItem("app_id")
    var acc_id = localStorage.getItem("acc_id")
    if(app_id){
        if(acc_id){
            verified = localStorage.getItem("verification")
            if(`${verified}`==="true"){
                UpDownLoad()
                setInterval(()=>{
                    console.log("presetting")
                    UpDownLoad()
                }, 10000)
                preSets()
                screenManager(2)
            }else{
                screenManager(10)
            }
            
        }else{
            screenManager(0)
        }
    }else{
        var url = `${home_url}/newDownload`
        var count = 0
        var reloader
        fetch(url, setOptioins({
            "new_born_key": new_born_key
        }))
        .then(x=>x.json())
        .then(y=>{
            if(y["state"]){
                localStorage.setItem("app_id", y["app_id"])
                clearInterval(reloader)
            }
        })
        .catch(()=>{
            Messanger(true, "Internet Connection Error")
            reloader = setInterval(()=>{
                AppInit()
                count +=1
            }, 10000)
        })
        screenManager(0)
    }

}

function preSets(){
    var history = localStorage.getItem("history")
    if(history){
        var all_history = document.getElementById("all_history")
        history = JSON.parse(history)
        history.forEach(element=>{
            var unit_histo = document.createElement("div")
            unit_histo.setAttribute("class", "unit_history")
            var subject = document.createElement("p")
            subject.innerHTML = element["subject"]
            var body = document.createElement("p")
            body.innerHTML = element["body"]
            var datetime = document.createElement("p")
            datetime.innerHTML = element["datetime"]
            var email_sms = document.createElement("div")
            if(element["email"]){
                var email = document.createComment("img")
                email.src = "img/email.png"
                email_sms.appendChild(email)
            }
            if(element["sms"]){
                var sms = document.createComment("img")
                sms.src = "img/sms.png"
                email_sms.appendChild(sms)
            }
            unit_histo.appendChild(subject)
            unit_histo.appendChild(body)
            unit_histo.appendChild(datetime)
            unit_histo.appendChild(email_sms)
            all_history.appendChild(unit_histo)

        })
    }

    var acc_details = JSON.parse(localStorage.getItem("acc_details"))
    if(localStorage.getItem("acc_details")){
        var institute_name = acc_details["name"]
        var institute_sms = acc_details["sms_id"]
        var institute_email = acc_details["email_id"]
        var institute_phone = acc_details["phone"]
        // var institute_pass = acc_details["app_pass"]
        var institute_state = acc_details["state"]
        var name_display = ["main_name_display_2", "main_name_display", "acc_name_display"]
        name_display.forEach(element=>{
            document.getElementById(element).innerHTML = institute_name
        })
        if(!institute_sms[0]){
            institute_sms[0] = "Not Set"
        }
        document.getElementById("acc_sms_details").innerHTML = `${institute_sms[0]} <br> ${institute_sms[1]}`
        document.getElementById("acc_email_details").innerHTML = `${institute_email[0]} <br> ${institute_email[1]}`

        document.getElementById("update_acc_name").value = institute_name
        document.getElementById("update_acc_pass").value = "0000 0000 0000 0000"
        document.getElementById("update_acc_no").value = institute_phone
        document.getElementById("update_acc_no_1").innerHTML = `#${institute_phone}`
        document.getElementById("acc_state").innerHTML = institute_state
        document.getElementById("acc_state_1").innerHTML = institute_state
    }

    var phone_book = JSON.parse(localStorage.getItem("phone_book"))
    if(phone_book){
        var total_contacts = 0
        var group_name = document.getElementById("group_name")
        group_name.innerHTML = ""
        var all_communities = document.getElementById("all_communities")
        all_communities.innerHTML = ""
        var all_contacts = document.getElementById("all_contacts")
        all_contacts.innerHTML = ""
        var count = 0
        unit_groups = []
        for(let x = 0; x < phone_book.length; x++){
            total_contacts+=phone_book[x]["magnitude"]
            var option = document.createElement("option")
            option.value = phone_book[x]["group_name"]
            option.innerHTML = phone_book[x]["group_name"]
            group_name.add(option)
    
            unit_groups[x] = document.createElement("div")
            unit_groups[x].setAttribute("class", "unit_group")
            unit_groups[x].addEventListener("click", ()=>{
                var current_state = ActiveSendCommunities(phone_book[x]["group_name"])
                if(current_state){
                    unit_groups[x].style.border = "2px solid var(--main_colour)"
                    unit_groups[x].style.background = "rgb(255, 186, 255)"
                }else{
                    unit_groups[x].style.border = "0 solid var(--main_colour)"
                    unit_groups[x].style.background = "rgb(213, 213, 213)"
                }
            })

            var unit_group_name = document.createElement("p")
            unit_group_name.innerHTML = phone_book[x]["group_name"]
            var unit_group_magnitude = document.createElement("p")
            unit_group_magnitude.innerHTML = `${phone_book[x]["magnitude"]} Contacts`
            // var edit_img = document.createElement("img")
            // edit_img.src = "img/edit.png"
            unit_groups[x].appendChild(unit_group_name)
            unit_groups[x].appendChild(unit_group_magnitude)
            // unit_groups[x].appendChild(edit_img)
            all_communities.appendChild(unit_groups[x])
            for(let y = 0; y < phone_book[x]["phone_book"].length; y++){
                var unit_contact = document.createElement("div")
                unit_contact.setAttribute("class", "unit_contact")
                var contact_name = document.createElement("p")
                contact_name.innerHTML = `${phone_book[x]["phone_book"][y]["name"]} (${phone_book[x]["phone_book"][y]["refcode"]})`
                var contact_group = document.createElement("p")
                contact_group.innerHTML = phone_book[x]["phone_book"][y]["group"]
                var contact_phone = document.createElement("p")
                contact_phone.innerHTML = phone_book[x]["phone_book"][y]["phone"]
                var contact_email = document.createElement("p")
                contact_email.innerHTML = phone_book[x]["phone_book"][y]["email"]
                var profile_img = document.createElement("img")
                profile_img.src = "img/profile.png"
                unit_contact.appendChild(contact_name)
                unit_contact.appendChild(contact_group)
                unit_contact.appendChild(contact_phone)
                unit_contact.appendChild(contact_email)
                unit_contact.appendChild(profile_img)
                all_contacts.appendChild(unit_contact)
            }
        }
        document.getElementById("no_of_contacts").innerHTML = `${total_contacts}`
        document.getElementById("no_of_communities").innerHTML = `${phone_book.length}`
        
    }else{
        UpDownLoad()
    }
}

function isStrongPassword(password){
    if(password.length < 8){
        return {
            "state": false,
            "message": "Password Length at Least 8"
        }
    }
    if(!/[A-Z]/.test(password)){
        return {
            "state": false,
            "message": "Password atleast one UpperCase Letter"
        }
    }
    if(!/[a-z]/.test(password)){
        return {
            "state": false,
            "message": "Password atleast one LowerCase Letter"
        }
    }
    if(!/\d/.test(password)){
        return {
            "state": false,
            "message": "Password atleast one number"
        }
    }
    if(!/[!@#$%^&*<>~`|]/){
        return {
            "state": false,
            "message": "Password atleast one symbole i.e !@#$%^&*<>~`|"
        }
    }

    return {
        "state": true
    }
}

function newAccountSetUp(){
    var newAccForm = document.forms["newAccount"]
    var fname = newAccForm["fname"]
    var lname = newAccForm["lname"]
    var phone = newAccForm["phone"]
    var email = newAccForm["email"]
    var password = newAccForm["password"]
    var confirm_password = newAccForm["confirm_password"]


    if(password.value != confirm_password.value){
        Messanger(true, "Password Miss match")
        return
    }

    password_test = isStrongPassword(password.value)
    if(!password_test["state"]){
        Messanger(true, password_test["message"])
        return
    }

    var NewAccForm = new FormData()
    NewAccForm.append("app_id", localStorage.getItem("app_id"))
    NewAccForm.append("fname", fname.value)
    NewAccForm.append("lname", lname.value)
    NewAccForm.append("phone", phone.value)
    NewAccForm.append("email", email.value)
    NewAccForm.append("password", password.value)

    var url = `${home_url}/signup`
    var options = {
        method: "POST",
        body: NewAccForm
    }
    Loading(true)
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        console.log(y)
        Loading(false)
        if(y["state"]){
            localStorage.setItem("acc_id", y["acc_id"])
            localStorage.setItem("acc_details", JSON.stringify({
                "name": fname.value+lname.value,
                "sms_id": ["Not Set", 0],
                "email_id": [email.value, 0],
                "app_pass": "<cloudstored>",
                "phone": phone.value,
                "state": "Inactive"
            }))
            localStorage.setItem("verification", false)
            preSets()
            screenManager(10)
        }else{
            Messanger(true, y["message"])
            screenManager(1)
        }
    })
    .catch((err)=>{
        Loading(false)
        console.log(err)
    })
}

function verifyAccount(){
    var code_form = document.forms["code_form"]
    var code_1 = code_form["code_1"].value
    var code_2 = code_form["code_2"].value
    var code_3 = code_form["code_3"].value
    var code_4 = code_form["code_4"].value
    var new_code = `${code_1}${code_2}${code_3}${code_4}`
    var ver_form = new FormData()
    ver_form.append("app_id", localStorage.getItem("app_id"))
    ver_form.append("acc_id", localStorage.getItem("acc_id"))
    ver_form.append("ver_code", new_code)
    var url = `${home_url}/verifyAccount`
    var options ={
        method: "POST",
        body: ver_form
    }
    Loading(true)
    fetch(url, options)
    .then(x=>x.json())
    .then(y=>{
        Loading(false)
        console.log(y)
        if(y["state"]){
            Messanger(true, y["message"])
            localStorage.setItem("verification", true)
            AppInit()
        }else{
            Messanger(true, y["message"])
        }
    })
    .catch(()=>{
        Loading(false)
        Messanger(true, "Please check your Internet Connection")
    })
}

function signIn(){
    var sign_in_form = document.forms["sign_in_form"]
    var email = sign_in_form["sign_in_email"]
    var password = sign_in_form["sign_in_password"]

    if(email.value.length != 0 && password.value.length != 0){
        var url = `${home_url}/signin`
        var data = {
            "app_id": localStorage.getItem("app_id"),
            "email": email.value,
            "password": password.value
        }
        Loading(true)
        fetch(url, setOptioins(data))
        .then(x=>x.json())
        .then(y=>{
            Loading(false)
            if(y["state"]){
                localStorage.setItem("app_id", y["app_id"])
                localStorage.setItem("acc_id", y["acc_id"])
                localStorage.setItem("phone_book", JSON.stringify(y["phone_book"]))
                localStorage.setItem("acc_details", JSON.stringify(y["acc_details"]))
                localStorage.setItem("verification", true)
                preSets()
                Messanger(true, "Successful Log In")
                screenManager(2)
            }else{
                Messanger(true, y["message"])
            }
        })
        .catch(()=>{
            Loading(false)
            Messanger(true, "Please Check your Internet Connection")
        })
    }
}

function PasswordReset(){
    console.log("Working")
    var sign_in_form = document.forms["sign_in_form"]
    var email = sign_in_form["sign_in_email"]
    if(email.value.length < 3){
        Messanger(true, "Please enter ONLY your email")
        return
    }
    var url = `${home_url}/restPassword`
    var data = {
        "app_id": localStorage.getItem("app_id"),
        "email": email.value
    }
    Loading(true)
    fetch(url, setOptioins(data))
    .then(x=>x.json())
    .then(y=>{
        Loading(false)
        console.log(y)
        if(y["state"]){
            Messanger(true, "REST Details Sent to Your Email")
        }
    })
    .catch(()=>{
        Messanger(true, "Please Check your Internet Connection")
    })

}

function setOptioins(data){
    return {
        method: "POST",
        headers:{
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }
}

function Loading(state){
    console.log("loading")
    if(state){
        loading_screen.style.display = "flex"
    }else{
        loading_screen.style.display = "none"
    }
}

function Messanger(state, message){
    var main_message = document.getElementById("main_message")
    if(state){
        alert_box.style.display = "flex"
        main_message.innerHTML = message
        setTimeout(()=>{
            alert_box.style.display = "none"
        }, 3500)
    }else{
        alert_box.style.display = "none"
        main_message.innerHTML = ""
    }
}

function newContact(){
    const new_contact = document.forms["new_contact"]
    var fname = new_contact["fname"]
    var lname = new_contact["lname"]
    var phone = new_contact["phone"]
    var email = new_contact["email"]
    var refcode = new_contact["refcode"]
    var group = new_contact["group_name"]
    console.log("aaaaaa")

    if(group.value == 0){
        Messanger(true, "No Communities Found \n Please create a Community")
        return
    }
    if(phone.value.length != 10){
        Messanger(true, "Contact length Invalid")
        return false
    }
    var contact_detail = {
        "name": `${fname.value} ${lname.value}`,
        "phone": phone.value,
        "email": email.value,
        "refcode": refcode.value,
        "group": group.value
    }
    var phone_book = JSON.parse(localStorage.getItem("phone_book"))
    for(let x = 0; x < phone_book.length; x++){
        if(phone_book[x]["group_name"]===group.value){
            phone_book[x]["phone_book"].push(contact_detail)
            phone_book[x]["magnitude"] +=1
            localStorage.setItem("phone_book", JSON.stringify(phone_book))
            document.getElementById("no_of_contacts").innerHTML = `${parseInt(document.getElementById("no_of_contacts").innerHTML)+1}`
            screenManager(5)
            Messanger(true, "Contact Added Successfully")
        }
    }
    fname.value = ""
    lname.value = ""
    phone.value = ""
    email.value = ""
    refcode.value = ""
    preSets()
    setTimeout(()=>{
        UpDownLoad()
    }, 3100)

}

function newGroup(){
    var group_name = prompt("Enter New group Name:")
    var phone_book = localStorage.getItem("phone_book") // Initially String
    var no_of_communities = document.getElementById("no_of_communities")
    console.log(group_name)
    if(group_name){
        var data = {
            "group_name": group_name,
            "magnitude": 0,
            "phone_book": []
        }
        if(phone_book){
            phone_book = JSON.parse(phone_book)
            for(let p = 0; p < phone_book.length; p++){
                if(phone_book[p]["group_name"]===group_name){
                    console.log("Match")
                    Messanger(true, "Community name Already Exists")
                    return
                }
            }
            phone_book.push(data)
            localStorage.setItem("phone_book", JSON.stringify(phone_book))
            no_of_communities.innerHTML = `${parseInt(no_of_communities.innerHTML)+1}`
            UpDownLoad()
            Messanger(true, "Community Saved Successfully")
        }else{
            phone_book = []
            phone_book.push(data)
            localStorage.setItem("phone_book", JSON.stringify(phone_book))
            no_of_communities.innerHTML = `${parseInt(no_of_communities.innerHTML)+1}`
            UpDownLoad()
            Messanger(true, "Group Saved Successfully")
        }
    }
    preSets()
}

function UpDownLoad(){
    var phone_book = localStorage.getItem("phone_book")
    if(phone_book){
        var url = `${home_url}/remoteStorage`
        var data = {
            "app_id": localStorage.getItem("app_id"),
            "acc_id": localStorage.getItem("acc_id"),
            "data": JSON.parse(localStorage.getItem("phone_book")),
            "arg": "upload"
        }
        fetch(url, setOptioins(data))
        .then(x=>x.json())
        .then(y=>{
            if(y["state"]){
                // Messanger(true, "Successfull")
                localStorage.setItem("phone_book", JSON.stringify(y["data"]))
                preSets()
            }else{
                Messanger(true, y["message"])
                preSets()
            }
            preSets()
        })
        .catch(()=>{
            Messanger(true, "Please Check your Internet Connection")
        })
    }else{
        var url = `${home_url}/remoteStorage`
        var data = {
            "app_id": localStorage.getItem("app_id"),
            "acc_id": localStorage.getItem("acc_id"),
            "data": "",
            "arg": "download"
        }
        Loading(true)
        fetch(url, setOptioins(data))
        .then(x=>x.json())
        .then(y=>{
            console.log(y)
            Loading(false)
            if(y["state"]){
                localStorage.setItem("phone_book", JSON.stringify(y["data"]))
                preSets()
                // Messanger(true, "Phone Book Successfully Downloaded")
            }else{
                Messanger(true, y["message"])
            }
            preSets()
        })
        .catch(()=>{
            Loading(false)
            Messanger(true, "Please Check your Internet Connection")
        })
    }
}

function ActiveSendCommunities(name){
    var now_group = name
    var state = true
    sendToCommunities.forEach(element=>{
        if(element === name){
            console.log("Already Exists ...")
            state = false
        }
    })

    if(state){
        sendToCommunities.push(name)
        console.log(sendToCommunities)
    }else{
        sendToCommunities.splice(sendToCommunities.indexOf(name), 1);
        console.log(sendToCommunities)
    }

    var add_new_group_btn = document.getElementById("add_new_group_btn")
    var delete_old_group_btn = document.getElementById("delete_old_group_btn")
    if(sendToCommunities.length == 1){
        add_new_group_btn.style.display = "none"
        delete_old_group_btn.style.display = "flex"
    }else if(sendToCommunities.length == 0){
        add_new_group_btn.style.display = "flex"
        delete_old_group_btn.style.display = "none"
    }


    if(sendToCommunities.length > 0){
        document.getElementById("send_to_btn").style.display = "flex"
    }else{
        document.getElementById("send_to_btn").style.display = "none"
    }
    return state
}

function deleteCommunities(){
    if(confirm(`Are you sure to Delete Community: ${sendToCommunities}`)){
        var phone_book = JSON.parse(localStorage.getItem("phone_book"))
        var new_phone_book = []
        var state = true
        phone_book.forEach(element_1=>{
            sendToCommunities.forEach(element_2=>{
                if(element_1["group_name"] == element_2){
                    console.log(`delete following : ${element_2}`)
                    state = false
                }
            })
            if(state){
                new_phone_book.push(element_1)
            }
            state = true
        })
        var add_new_group_btn = document.getElementById("add_new_group_btn")
        var delete_old_group_btn = document.getElementById("delete_old_group_btn")
        var send_to_btn = document.getElementById("send_to_btn")
        add_new_group_btn.style.display = "flex"
        delete_old_group_btn.style.display = "none"
        send_to_btn.style.display = "none"
        // sendToCommunities = []
        console.log(new_phone_book)
        localStorage.setItem("phone_book", JSON.stringify(new_phone_book))
        preSets()
        var url = `${home_url}/phoneBookModify`
        var data = {
            "app_id": localStorage.getItem("app_id"),
            "acc_id": localStorage.getItem("acc_id"),
            "deltype": "group",
            "groups": sendToCommunities
        }
        sendToCommunities = []
        fetch(url, setOptioins(data))
        .then(x=>x.json())
        .then(y=>{
            console.log(y)
            if(y["state"]){
                localStorage.setItem("phone_book", JSON.stringify(y["phone_book"]))
                preSets()
                Messanger(true, "Successful")
            }else{
                Messanger(true, "Sorry, an Error Occured")
            }
        })
    }
}   

function ContactSearch(){
    var search_bar = document.getElementById("contact_search").value
    console.log(search_bar)
    if(search_bar.length == 0){
        preSets()
        return
    }
    Loading(true)
    var phone_book = JSON.parse(localStorage.getItem("phone_book"))
    var results = []
    let x = 0
    for(x = 0; x < phone_book.length; x++){
        let y = 0
        for(y = 0; y < phone_book[x]["phone_book"].length; y++){
            var data_sets = []
            data_sets.push(phone_book[x]["phone_book"][y]["name"].split(" ")[0])
            data_sets.push(phone_book[x]["phone_book"][y]["name"].split(" ")[1])
            data_sets.push(phone_book[x]["phone_book"][y]["phone"])
            data_sets.push(phone_book[x]["phone_book"][y]["refcode"])
            data_sets.forEach(element=>{
                element = `${element.toUpperCase()}`
                if(element.startsWith(search_bar.toUpperCase())){
                    results.push(phone_book[x]["phone_book"][y]);
                }
            })
        }
    }
    Loading(false)
    console.log(results)
    var all_contacts = document.getElementById("all_contacts")
    all_contacts.innerHTML = ""
    for(let y = 0; y < results.length; y++){
        var unit_contact = document.createElement("div")
        unit_contact.setAttribute("class", "unit_contact")
        var contact_name = document.createElement("p")
        contact_name.innerHTML = `${results[y]["name"]} (${results[y]["refcode"]})`
        var contact_group = document.createElement("p")
        contact_group.innerHTML = results[y]["group"]
        var contact_phone = document.createElement("p")
        contact_phone.innerHTML = results[y]["phone"]
        var contact_email = document.createElement("p")
        contact_email.innerHTML = results[y]["email"]
        var profile_img = document.createElement("img")
        profile_img.src = "img/profile.png"
        unit_contact.appendChild(contact_name)
        unit_contact.appendChild(contact_group)
        unit_contact.appendChild(contact_phone)
        unit_contact.appendChild(contact_email)
        unit_contact.appendChild(profile_img)
        all_contacts.appendChild(unit_contact)
    }
}

function sendBulkie(){
    const send_details = document.forms["send_details"]
    var email = send_details["send_email"].checked
    var sms = send_details["send_sms"].checked
    var subject = send_details["send_subject"].value
    var body = send_details["send_body"].value
    var schedule_div = document.getElementById(`schedule_timer`).style.display
    var schedule = send_details["send_schedule"].value
    var message_details = {
        "acc_id": localStorage.getItem("acc_id"),
        "app_id": localStorage.getItem("app_id"),
        "groups": sendToCommunities,
        "sms": false,
        "email": false,
        "subject": subject,
        "body": body,
        "schedule": false
    }

    if (schedule_div == "flex" && schedule.length > 2){
        message_details.schedule = schedule
    }else{
        message_details.schedule = false
    }

    if(!email && !sms){
        Messanger(true, "Sending Provider Missing: Emal/SMS")
        return false
    }
    if(email){
        message_details["email"] = true
    }
    if(sms){
        message_details["sms"] = true
    }

    console.log(message_details)
    var url = `${home_url}/APISend`
    Loading(true)
    fetch(url, setOptioins(message_details))
    .then(x=>x.json())
    .then(y=>{
        console.log(y)
        Loading(false)
        if(y["state"]){
            Messanger(true, y["message"])
            var history = localStorage.getItem("history")
            var new_history = {
                "subject": message_details["subject"],
                "body": message_details["body"],
                "datetime": getCurrentDatetime(),
                "email": message_details["email"],
                "sms": message_details["sms"]
            }
            if(history){
                history = JSON.parse(history)
                history.push(new_history)
                history = JSON.stringify(history)
                localStorage.setItem("history", history)
            }else{
                history = JSON.stringify([new_history])
                localStorage.setItem("history", history)
            }
            if(email){
                send_details["send_subject"].value = ""
                send_details["send_body"].value = ""
                send_details["send_schedule"].value = ""
            }
            if(sms){
                send_details["send_subject"].value = ""
                send_details["send_body"].value = ""
                send_details["send_schedule"].value = ""
            }
            preSets()
        }else{
            Messanger(true, y["message"])
            screenManager(7)
        }
    })
    .catch(()=>{
        Loading(false)
        Messanger(true, "Please Check Internet Connection")
    })
}

function ActivateSchedule(element){
    var dom_element = document.getElementById(`schedule_timer`)
    var current_display = dom_element.style.display
    if(current_display == "none"){
        dom_element.children[1].setAttribute("required", true)
        element.style.background = "rgb(205, 0, 205)"
        element.style.width = "100%"
        dom_element.style.display = "flex"
    }else{
        dom_element.children[1].removeAttribute("required")
        element.style.background = "gray"
        dom_element.style.display = "none"
        element.style.width = "40%"
    }
}

function EditAccount(state){
    var current_src = document.getElementById("enable_edit_btn").src.split("/")
    current_src = current_src[4]
    if(state){
        if(current_src == "edit.png"){
            var update_inputs = ["update_acc_name", "update_acc_pass", "update_acc_no"]
            update_inputs.forEach(element=>{
                document.getElementById(element).removeAttribute("readOnly")
                document.getElementById(element).style.background = "rgb(205, 0, 205)"
            })
            document.getElementById("update_acc_pass").setAttribute("type", "text")
            document.getElementById("enable_edit_btn").src = "img/cancel.png"
            document.getElementById("account_edit_update").style.display = "flex"
            Messanger(true, "Editing Enabled ...")
        }else{
            var update_inputs = ["update_acc_name", "update_acc_pass", "update_acc_no"]
            update_inputs.forEach(element=>{
                document.getElementById(element).setAttribute("readOnly", true)
                document.getElementById(element).style.background = "transparent"
            })
            document.getElementById("update_acc_pass").setAttribute("type", "password")
            document.getElementById("enable_edit_btn").src = "img/edit.png"
            document.getElementById("account_edit_update").style.display = "none"
            Messanger(true, "Editing Disabled ...")
        }
    }else{
        var updates_form = document.forms["account_updates"]
        var name = updates_form["update_acc_name"].value
        var app_pass = updates_form["update_acc_pass"].value
        var phone = updates_form["update_acc_no"].value
        var url = `${home_url}/updateAccount`
        var acc_details = {
            "app_id": localStorage.getItem("app_id"),
            "acc_id": localStorage.getItem("acc_id"),
            "name": name,
            "app_pass": app_pass,
            "phone": phone,
        }
        console.log("Updating ...")
        Loading(true)
        fetch(url, setOptioins(acc_details))
        .then(x=>x.json())
        .then(y=>{
            Loading(false)
            if(y["state"]){
                var new_acc_details = y["updates"]
                localStorage.setItem("acc_details", JSON.stringify(new_acc_details))
                preSets()
                Messanger(true, "Account Updates Successfully")
                setTimeout(()=>{
                    EditAccount(true)
                }, 2000)
            }else{
                Messanger(true, y["message"])
            }
        })
        .catch(()=>{
            Loading(false)
            Messanger(true, "Please check Internet Connection")
        })
    }
}

function getCurrentDatetime(){
    var datetime = new Date()
    year = `${datetime.getFullYear()}`
    month = `${datetime.getMonth()+1}`
    date = `${datetime.getDate()}`
    hour = `${datetime.getHours()}`
    minute = `${datetime.getMinutes()}`
    datetime = `${year}-${month}-${date} ${hour}:${minute}`
    console.log(datetime)
    return datetime
}

function logOut(){
    localStorage.clear()
    Messanger(true, "Logged Out Successfully")
    setTimeout(()=>{
        location.reload()
    }, 3000)
}
