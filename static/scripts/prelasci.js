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


    // // set onclick events for start
    // setEvents(START, startOtherOptionsDiv)
    // // set onclick events for end
    // setEvents(END, endOtherOptionsDiv)
}

function setEvens(where, optionsDiv) {
    options = optionsDiv.childNodes

    for (let option of options) {
        option.onclick = (e) => {
            let node = e.target

            setNewOption(where, node.innerText)
        }
    }
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

    let sysData = fetch(url, params).then(response => {
        return response.json()
    })


    return sysData
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
    // return `<a class="dropdown-item" href="#" onclick="setNewOption(${where}, '${text}')">${text}</a>`

    let a = document.createElement("a")
    a.classList.add("dropdown-item")
    a.setAttribute("href", "#")
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
        inputBox.innerHTML += makeInput(input)
    }
}

function makeInput(name) {
    const input = `

    <div class="input-group mb-4">
        <input type="text" class="form-control" id="${name}"
               aria-label="${name} name="${name}" aria-describedby="basic-addon2">
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
            // Fill in the results
            for (outputId in res) {
                document.getElementById(outputId).value = res[outputId]
            }
        })
}

function parseSystemInputs() {
    let startSystem = systems[startOptionText]

    let inputData = {}


    for (inputID of startSystem.inputs) {
        let input = document.getElementById(inputID)

        inputData[inputID] = input.value
    }


    let data = {
        startName: startOptionText,
        startData: inputData,
        endName: endOptionText,
    }

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
