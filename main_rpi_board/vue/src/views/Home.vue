<template>
  <div class="home">
    <div v-if="!isMobile()">
      <p>Loftslamper</p>
      <button type = "button" v-on:click="ikea_lights('On')">Tænd</button>
      <button type = "button" v-on:click="ikea_lights('Off')">Sluk</button><br>
      <p>Dæmpning</p>
      <button type = "button" v-on:click="ikea_lights(25)">25</button>
      <button type = "button" v-on:click="ikea_lights(50)">50</button>
      <button type = "button" v-on:click="ikea_lights(75)">75</button>
      <button type = "button" v-on:click="ikea_lights(100)">100</button><br>
      <p>Skrivebords lampe</p>
      <button type = "button" v-on:click="relay(0, 'desk', 'On')">Tænd</button>
      <button type = "button" v-on:click="relay(0, 'desk', 'Off')">Sluk</button><br>
      <p>Lys kæde</p>
      <button type = "button" v-on:click="relay(1, 'chain', 'On')">Tænd</button>
      <button type = "button" v-on:click="relay(1, 'chain', 'Off')">Sluk</button><br>
    </div>
    <div v-else>
      <p style="font-size : 25px;">Loftslamper</p>
      <button type = "button" class="buttonMobile" v-on:click="ikea_lights('On')">Tænd</button>
      <button type = "button" class="buttonMobile" v-on:click="ikea_lights('Off')">Sluk</button><br>
      <p style="font-size : 25px;">Dæmpning</p>
      <button type = "button" class="buttonMobile" v-on:click="ikea_lights(25)">25</button>
      <button type = "button" class="buttonMobile" v-on:click="ikea_lights(50)">50</button><br>
      <button type = "button" class="buttonMobile" v-on:click="ikea_lights(75)">75</button>
      <button type = "button" class="buttonMobile" v-on:click="ikea_lights(100)">100</button><br>
      <p style="font-size : 25px;">Skrivebords lampe</p>
      <button type = "button" class="buttonMobile" v-on:click="relay(0, 'desk', 'On')">Tænd</button>
      <button type = "button" class="buttonMobile" v-on:click="relay(0, 'desk', 'Off')">Sluk</button><br>
      <p style="font-size : 25px;">Lys kæde</p>
      <button type = "button" class="buttonMobile" v-on:click="relay(1, 'chain', 'On')">Tænd</button>
      <button type = "button" class="buttonMobile" v-on:click="relay(1, 'chain', 'Off')">Sluk</button><br>
    </div>   
  </div>
</template>

<style scoped>
.buttonMobile {
  width: 100px;
  height: 50px;
  margin-right: 5px;
  margin-left: 5px;
  margin-bottom: 5px;
  border-radius: 10px;
  background: #17c9e3;
  font-size : 20px;
  }
</style>

<script>
export default {
  name: 'Home',
  methods : {
    ikea_lights : function(value){
      if(typeof(value) == "string"){
        this.fetchAPICall(0, "ikea_lights?state=" + value, "GET");
      }
      else if(typeof(value) == "number"){
        this.fetchAPICall(0, "ikea_lights?value=" + value, "GET");
      }
    },
    relay : function (dest, light, state){ 
      this.fetchAPICall(dest, "relay?state=" + String(state) + "&light_source=" + String(light), "GET")
    },
    fetchAPICall : async function (board, route, method) {
      let url = (board == 1 ? "http://192.168.0.165:3000/" + route : "http://192.168.0.101:3000/" + route)
      console.log(url);
      try {
        return await fetch(url, { method: method });
      } 
      catch (err) {
        alert("Error: " + err);
      }
    },
    isMobile() {
      if(/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        return true
      } else {
        return false
      }
    }
  }
}
</script>
