<template>
  <div class="serviceedit">
    <b-container fluid>
      <!-- service title -->
      <b-row class="service-title">
        <b-col sm="2"><label for="input-large">Title</label></b-col>
        <b-col sm="10">
          <b-form-input id="input-large" size="lg" type="text" placeholder="Enter service title"> {{ title }}</b-form-input>
        </b-col>
      </b-row>
      <!-- service major picture-->
      <b-row class="service-title">
        <b-col sm="2"><label for="input-large">Major Pic</label></b-col>
        <b-col sm="10">
          <b-img src="file://///home/ubuntu/Pictures/index.png" fluid-grow alt="Responsive image" />
        </b-col>
      </b-row>
    </b-container>
  </div>
</template>

<script>
  import PictureInput from './PictureInput.vue'
  export default {
    name: 'ServiceEdit',
    data () {
      return {
        title: '7 days finishing'
      }
    },
    components: {
      'picture-input': PictureInput
    }
  }
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
  h1,
  h2 {
    font-weight: normal;
  }
  
  ul {
    list-style-type: none;
    padding: 0;
  }
  
  li {
    display: inline-block;
    margin: 0 10px;
  }
  
  a {
    color: #42b983;
  }
</style>

