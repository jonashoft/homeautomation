<template>
  <div class="hello">
      <p class="chain"> Lyskæde</p>
      <input class="apple-switch" type="checkbox" id="chainSwitch" @change="checkboxUpdate('chain')" v-model="chainState"><br>

      <br><p> Værelse</p><br>
      <input class="apple-switch" type="checkbox" id="roomSwitch" @change="checkboxUpdate('room')" v-model="roomState">
      <input class="range" type="range" id="roomSlider" name="vol" min="0" max="100" step="1" @change="sliderUpdate('room')" v-model="roomValue"><br>
      <br><p> Gang</p><br>
      <input class="apple-switch" type="checkbox" id="hallSwitch" @change="checkboxUpdate('hall')" v-model="hallState">
      <input class="range" type="range" id="hallSlider" name="vol" min="0" max="100" step="1" @change="sliderUpdate('hall')" v-model="hallValue"><br>
      <br><p> Toilet</p><br>
      <input class="apple-switch" type="checkbox" id="toiletSwitch" @change="checkboxUpdate('toilet')" v-model="toiletState">
      <input class="range" type="range" id="toiletSlider" name="vol" min="0" max="100" step="1" @change="sliderUpdate('toilet')" v-model="toiletValue"><br>
  </div>
</template>

<script>
    export default {
        name: 'ToggleSwitches',
        methods:{
            sliderUpdate : function(destination){
                switch (destination){
                    case 'room':
                        this.connection.send(JSON.stringify({roomValue:this.roomValue}))
                        break;
                    case 'hall':
                        this.connection.send(JSON.stringify({hallValue:this.hallValue}))
                        break;
                    case 'toilet':
                        this.connection.send(JSON.stringify({toiletValue:this.toiletValue}))
                        break;
                    default:
                        console.log("Error - unknown destination")
                }
            },
            checkboxUpdate : function(destination){
                switch (destination){
                    case 'room':
                        this.connection.send(JSON.stringify({roomState:this.roomState}))
                        break;
                    case 'hall':
                        this.connection.send(JSON.stringify({hallState:this.hallState}))
                        break;
                    case 'toilet':
                        this.connection.send(JSON.stringify({toiletState:this.toiletState}))
                        break;
                    case 'chain':
                        this.connection.send(JSON.stringify({chainState:this.chainState}))
                        break;
                    default:
                        console.log("Error - unknown destination")
                }
            }
        },
        data() {
          return { roomValue: 75, hallValue: 50, toiletValue: 25, roomState: true, hallState: true, toiletState: false, chainState: true}
        },
        created: function() {
            console.log("Starting connection to WebSocket Server")
            this.connection = new WebSocket("ws://localhost:3000/")

            let self = this; // this is required to access the correct scope inside the callback
            this.connection.onmessage = function(event) {
                let received = JSON.parse(event.data);
                console.log(received)
                if ({}.propertyIsEnumerable.call(received, 'roomState')){
                    self.roomState = received.roomState;
                }
                if ({}.propertyIsEnumerable.call(received, 'roomValue')){
                    self.roomValue = received.roomValue;
                }
                if ({}.propertyIsEnumerable.call(received, 'toiletState')){
                    self.toiletState = received.toiletState;
                }
                if ({}.propertyIsEnumerable.call(received, 'toiletValue')){
                    self.toiletValue = received.toiletValue;
                }
                if ({}.propertyIsEnumerable.call(received, 'hallState')){
                    self.hallState = received.hallState;
                }
                if ({}.propertyIsEnumerable.call(received, 'hallValue')){
                    self.hallValue = received.hallValue;
                }
                if ({}.propertyIsEnumerable.call(received, 'chainState')){
                    self.chainState = received.chainState;
                }
            }

            this.connection.onopen = function(event) {
                console.log(event)
            }

        }
    }
</script>

<style scoped>
p{
    display: inline-block;
    vertical-align: middle;
    font-weight: bold;
    font-size: large;
    font-family: Arial, Helvetica, sans-serif;
}
p.chain{
    margin-right: 20px;
}

input.apple-switch {
  position: relative;
  -webkit-appearance: none;
  outline: none;
  width: 50px;
  height: 30px;
  background-color: #fff;
  border: 1px solid #D9DADC;
  border-radius: 50px;
  box-shadow: inset -20px 0 0 0 #fff;
  display: inline-block;
vertical-align: middle;
}

input.apple-switch:after {
  content: "";
  position: absolute;
  top: 1px;
  left: 1px;
  background: transparent;
  width: 26px;
  height: 26px;
  border-radius: 50%;
  box-shadow: 2px 4px 6px rgba(0,0,0,0.2);
}

input.apple-switch:checked {
  box-shadow: inset 20px 0 0 0 #4ed164;
  border-color: #4ed164;
}

input.apple-switch:checked:after {
  left: 20px;
  box-shadow: -2px 4px 3px rgba(0,0,0,0.05);
}
input.range{
    -webkit-appearance: none;
    background: #fff;
    height: 5px;
    width: 200px;
    border-radius: 50px;
    margin-left: 20px;
    position: relative;

    display: inline-block;
    vertical-align: middle;

    border: 1px solid #D9DADC;
    box-shadow: inset -20px 0 0 0 #fff;
}
input.range::-webkit-slider-thumb {
  -webkit-appearance: none; /* Override default look */
  appearance: none;
  width: 25px; /* Set a specific slider handle width */
  height: 25px; /* Slider handle height */
  border-radius: 50%;
  background: #4ed164; /* Green background */
  cursor: pointer; /* Cursor on hover */
}

input.range::-moz-range-thumb {
  width: 25px; /* Set a specific slider handle width */
  height: 25px; /* Slider handle height */
  background: #4ed164; /* Green background */
  cursor: pointer; /* Cursor on hover */
}

</style>