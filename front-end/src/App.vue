<template>
  <!--<HelloWorld msg="Welcome to Your Vue.js App"/>-->
  
  <ToggleSwitches/>
</template>

<script>
import ToggleSwitches from './components/ToggleSwitches.vue'

export default {
  name: 'App',
  components: {
    ToggleSwitches
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
