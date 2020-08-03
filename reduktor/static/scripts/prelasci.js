const START = "start"
const END = "end"

var systems = {}

// Get element of the starting coordinate system
let startOptionText = "Nebesko ekvatorski"
var startCurrentOptionDiv = document.getElementById("start-system-btn")
// Get other starting options
var startOtherOptionsDiv = document.getElementById("start-options")
var startInputBox = document.getElementById("inputBox")

// Get element of the ending coordinate system
let endOptionText = "Horizontski"
var endCurrentOptionDiv = document.getElementById("end-system-btn")
// Get other ending options
var endOtherOptionsDiv = document.getElementById("end-options")
var endInputBox = document.getElementById("outputBox")


init()


// Set the event handler for transform button
document.getElementById("transform").addEventListener("click", transform)

function init() {
    initSystems()
}

async function initSystems() {
    systems = await getSystemsData()

    fillOtherOptions(START)
    fillOtherOptions(END)

    fillInputs(START)
    fillInputs(END)
}

async function getSystemsData() {
    const url = "/prelasci/all_systems_info"

    const params = {
        headers: {
            "content-type": "application/json; charset=UTF-8"
        },
        method: "POST"
    }

    return fetch(url, params).then(response => {
        return response.json()
    })
}

function setNewOption(where, newOptionText) {
    if (where === START) {
        startOptionText = newOptionText
    } else if (where === END) {
        endOptionText = newOptionText
    } else {
        alert("WRONG!")
        return
    }

    resetNavOptions()

    fillOtherOptions(END)
    fillOtherOptions(START)

    fillInputs(START)
    fillInputs(END)
}

// Fill drow-down menu options for start or end system
function fillOtherOptions(where) {
    let optionsDiv

    if (where === START) {
        optionsDiv = startOtherOptionsDiv
        startCurrentOptionDiv.innerText = startOptionText
    } else if (where === END) {
        optionsDiv = endOtherOptionsDiv
        endCurrentOptionDiv.innerText = endOptionText
    } else {
        alert("ERROR!")
        return
    }

    // Exclude system names that are already selected
    let systemNames = Object.keys(systems)
    let tmpSystems = new Set(systemNames)
    tmpSystems.delete(startOptionText)
    tmpSystems.delete(endOptionText)
    let systemArr = [...tmpSystems]

    // clear parent div
    optionsDiv.innerHTML = ""


    // Fill with children
    while (systemArr.length) {
        let newOption = makeOption(where, systemArr.pop())
        optionsDiv.appendChild(newOption)
    }

}

function makeOption(where, text) {
    let a = document.createElement("a")
    a.classList.add("dropdown-item")
    a.addEventListener("click", (e) => {
        setNewOption(where, text)
    })
    a.innerText = text

    return a
}


function fillInputs(where) {
    let inputBox = undefined
    let system = undefined

    if (where === START) {

        inputBox = startInputBox
        system = {
            name: startOptionText,
            inputs: systems[startOptionText].inputs
        }
    } else if (where === END) {
        inputBox = endInputBox
        system = {
            name: endOptionText,
            inputs: systems[endOptionText].outputs
        }
    } else {
        alert("NO NO NO!!")
        return
    }

    inputBox.innerHTML = ""
    for (let input of system.inputs) {
        inputBox.innerHTML += makeInput(where, input)
    }

    if (where == START) {
        inputBox.children[0].children[0].select()

    }


}

function makeInput(where, name) {
    const input = `

    <div class="input-group mb-4">
        <input type="text" class="form-control" id="${where}-${name}"
               aria-label="${where}-${name} name="${where}-${name}" aria-describedby="basic-addon2">
        <div class="input-group-append">
            <span class="input-group-text" id="basic-addon2">${name}</span>
        </div>
    </div>
    `

    return input
}


function transform() {
    // Spin astro logo
    andYetItMoves()

    let data = parseSystemInputs()

    console.log(data)


    let url = "/prelasci/transformisi"

    const params = {
        headers: {
            "content-type": "application/json; charset=UTF-8"
        },
        body: JSON.stringify(data),
        method: "POST"
    }

    fetch(url, params)
        .then(data => {
            return data.json()
        })
        .then(res => {
            res = JSON.parse(res)
            console.log("res: ")
            console.log(res)
            // Fill in the results
            for (let outputId in res) {
                document.getElementById(`end-${outputId}`).value = res[outputId]
            }
        })
}

function parseSystemInputs() {
    let startSystem = systems[startOptionText]

    // User input data
    let inputData = {}
    for (let inputID of startSystem.inputs) {
        let input = document.getElementById(`start-${inputID}`)

        inputData[inputID] = input.value
    }

    // navbar options
    precessionSwitch = document.getElementById("precesijaSwitch")
    nutationSwitch = document.getElementById("nutacijaSwitch")
    geoTopSwitch = document.getElementById("geoTopoSwitch")

    options = {}
    options.PREC = precessionSwitch.checked
    options.NUT = nutationSwitch.checked
    if (geoTopSwitch.checked) {
        options.GEO_TOPO = {}

        options.GEO_TOPO.lon = document.getElementById("start-longituda").value
        options.GEO_TOPO.h = document.getElementById("start-visina").value
        options.GEO_TOPO.r = document.getElementById("start-udaljenost").value
    } else {
        options.GEO_TOPO = false
    }

    let data = {
        startName: startOptionText,
        startData: inputData,
        endName: endOptionText,
        options: options
    }


    console.log(options)

    return data
}

let rotation = 80

function andYetItMoves() {
    let ball = document.getElementById("corner-logo-top")

    rotation += 360
    ball.style.transform = `rotate(${rotation}deg)`

    if (rotation > 1000)
        rotation = 80
}

function resetNavOptions() {
    document.getElementById("precesijaSwitch").checked = false
    document.getElementById("nutacijaSwitch").checked = false
    document.getElementById("geoTopoSwitch").checked = false
}

// functions for nav form inputs
document.getElementById("geoTopoSwitch").addEventListener("click", (e) => {
    if (e.target.checked) {
        console.log("HEY")
        let startInputs = document.getElementById("inputBox")
        startInputs.innerHTML += makeInput(START, "visina")
        startInputs.innerHTML += makeInput(START, "longituda")
        startInputs.innerHTML += makeInput(START, "udaljenost")
    } else {
        let visinaIn = document.getElementById("start-visina")
        let longitudaIn = document.getElementById("start-longituda")
        let udaljenost = document.getElementById("start-udaljenost")

        visinaIn.parentElement.remove()
        longitudaIn.parentElement.remove()
        udaljenost.parentElement.remove()
    }
})

window.addEventListener("keyup", (e) => {
    if (e.key === "Enter") transform()
})

