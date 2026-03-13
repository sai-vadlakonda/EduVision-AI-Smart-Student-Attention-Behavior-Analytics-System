/* ============================= */
/* ATTENTION CHART */
/* ============================= */

const attentionChart = new Chart(
document.getElementById("attentionChart"),
{
type:"line",

data:{
labels:[],
datasets:[
{
label:"Attention",
data:[],
borderColor:"#2563eb",
backgroundColor:"rgba(37,99,235,0.1)",
tension:0.3,
fill:true
}
]
},

options:{
animation:false,
responsive:true,
maintainAspectRatio:false,

scales:{
y:{
min:0,
max:1,
ticks:{
stepSize:0.2
}
}
}
}
});


/* ============================= */
/* EMOTION CHART */
/* ============================= */

const emotionChart = new Chart(
document.getElementById("emotionChart"),
{
type:"pie",

data:{
labels:[],
datasets:[
{
data:[],
backgroundColor:[
"#22c55e",
"#facc15",
"#ef4444",
"#3b82f6",
"#a855f7"
]
}
]
},

options:{
responsive:true,
maintainAspectRatio:false
}
});


/* ============================= */
/* UPDATE STATS */
/* ============================= */

async function updateStats(){

const res = await fetch("http://127.0.0.1:8000/stats")
const data = await res.json()

document.getElementById("students").innerText=data.students
document.getElementById("attention").innerText=data.attention
document.getElementById("phones").innerText=data.phones
document.getElementById("productivity").innerText=data.productivity

attentionChart.data.labels.push(new Date().toLocaleTimeString())
attentionChart.data.datasets[0].data.push(data.attention)

if(attentionChart.data.labels.length>20){

attentionChart.data.labels.shift()
attentionChart.data.datasets[0].data.shift()

}

attentionChart.update()

}



/* ============================= */
/* ALERTS */
/* ============================= */

async function updateAlerts(){

const res = await fetch("http://127.0.0.1:8000/alerts")
const alerts = await res.json()

const box = document.getElementById("alerts")

box.innerHTML=""

alerts.slice(-10).reverse().forEach(a=>{

box.innerHTML+=`<p>${a}</p>`

})

}



/* ============================= */
/* EMOTIONS */
/* ============================= */

async function updateEmotions(){

const res = await fetch("http://127.0.0.1:8000/emotions")
const emotions = await res.json()

emotionChart.data.labels=Object.keys(emotions)
emotionChart.data.datasets[0].data=Object.values(emotions)

emotionChart.update()

}



/* ============================= */
/* PHONE VIOLATIONS */
/* ============================= */

async function updatePhoneLogs(){

const res = await fetch("http://127.0.0.1:8000/phone_logs")
const logs = await res.json()

const tbody=document.querySelector("#phoneTable tbody")

tbody.innerHTML=""

logs.slice(-10).reverse().forEach(log=>{

const imgURL = log.ImageURL + "?t=" + Date.now()

tbody.innerHTML+=`

<tr>

<td>${log.Time}</td>

<td>${log.RollNo}</td>

<td>${log.Student}</td>

<td>

<a href="${imgURL}" target="_blank">

<img src="${imgURL}"
style="
width:70px;
height:50px;
object-fit:cover;
border-radius:6px;
border:1px solid #ddd;
cursor:pointer;
">

</a>

</td>

</tr>

`

})

}



/* ============================= */
/* DASHBOARD REFRESH */
/* ============================= */

function refreshDashboard(){

updateStats()
updateAlerts()
updateEmotions()
updatePhoneLogs()

}

setInterval(refreshDashboard,2000)

refreshDashboard()