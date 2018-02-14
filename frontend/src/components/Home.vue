
<template>
  <div>
  <div> <!-- nav bar -->
  <b-navbar toggleable="md" type="dark" variant="info">
  <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
  <b-navbar-brand href="#">NavBar</b-navbar-brand>
  <b-collapse is-nav id="nav_collapse">
    <b-navbar-nav>
      <b-nav-item href="#">Link</b-nav-item>
      <b-nav-item href="#" disabled>Disabled</b-nav-item>
    </b-navbar-nav>

    <!-- Right aligned nav items -->
    <b-navbar-nav class="ml-auto">

      <b-nav-form>
        <b-form-input size="sm" class="mr-sm-2" type="text" placeholder="Search"/>
        <b-button size="sm" class="my-2 my-sm-0" type="submit">Search</b-button>
      </b-nav-form>

      <b-nav-item-dropdown text="Lang" right>
        <b-dropdown-item href="#">EN</b-dropdown-item>
        <b-dropdown-item href="#">ES</b-dropdown-item>
        <b-dropdown-item href="#">RU</b-dropdown-item>
        <b-dropdown-item href="#">FA</b-dropdown-item>
      </b-nav-item-dropdown>

      <b-nav-item-dropdown right>
        <!-- Using button-content slot -->
        <template slot="button-content">
          <em>User</em>
        </template>
        <b-dropdown-item href="#">Profile</b-dropdown-item>
        <b-dropdown-item href="#">Signout</b-dropdown-item>
      </b-nav-item-dropdown>
    </b-navbar-nav>

  </b-collapse>
  </b-navbar>


  <b-carousel id="carousel1"
              style="text-shadow: 1px 1px 2px #333;"
              controls
              indicators
              background="#ababab"
              :interval="4000"
              img-width="1024"
              img-height="480"
              v-model="slide"
              @sliding-start="onSlideStart"
              @sliding-end="onSlideEnd"
  >

    <!-- Text slides with image -->
    <b-carousel-slide caption="First slide"
                      text="Nulla vitae elit libero, a pharetra augue mollis interdum."
                      img-src="https://lorempixel.com/1024/480/technics/2/"
    ></b-carousel-slide>

    <!-- Slides with custom text -->
    <b-carousel-slide img-src="https://lorempixel.com/1024/480/technics/4/">
      <h1>Hello world!</h1>
    </b-carousel-slide>

    <!-- Slides with image only -->
    <b-carousel-slide img-src="https://lorempixel.com/1024/480/technics/8/">
    </b-carousel-slide>

    <!-- Slides with img slot -->
    <!-- Note the classes .d-block and .img-fluid to prevent browser default image alignment -->
    <b-carousel-slide>
      <img slot="img" class="d-block img-fluid w-100" width="1024" height="480"
            src="https://lorempixel.com/1024/480/technics/5/" alt="image slot">
    </b-carousel-slide>

    <!-- Slide with blank fluid image to maintain slide aspect ratio -->
    <b-carousel-slide caption="Blank Image" img-blank img-alt="Blank image">
      <p>
        Lorem ipsum dolor sit amet, consectetur adipiscing elit. Suspendisse
        eros felis, tincidunt a tincidunt eget, convallis vel est. Ut pellentesque
        ut lacus vel interdum.
      </p>
    </b-carousel-slide>

  </b-carousel>
  </div>
  </div>
</template>

<script>
import axios from 'axios'
import { getBackendAPIURI } from './genlib.js'
export default {
  data () {
    return {
      randomNumber: 0,
      slide: 0,
      sliding: null
    }
  },
  methods: {
    getRandomInt (min, max) {
      min = Math.ceil(min)
      max = Math.floor(max)
      return Math.floor(Math.random() * (max - min + 1)) + min
    },
    getRandom () {
      // this.randomNumber = this.getRandomInt(1, 100)
      this.randomNumber = this.getRandomFromBackend()
    },
    getRandomFromBackend () {
      const path = getBackendAPIURI(window.location.href, '/api/random')
      axios.get(path)
      .then(response => {
        this.randomNumber = response.data.randomNumber
      })
      .catch(error => {
        console.log(error)
      })
    }
  },
  created () {
    this.getRandom()
  },
  onSlideStart (slide) {
    this.sliding = true
  },
  onSlideEnd (slide) {
    this.sliding = false
  }
}
</script>

<style>
  .el-carousel__item h3 {
    color: #475669;
    font-size: 14px;
    opacity: 0.75;
    line-height: 200px;
    margin: 0;
  }
  
  .el-carousel__item:nth-child(2n) {
    background-color: #99a9bf;
  }
  
  .el-carousel__item:nth-child(2n+1) {
    background-color: #d3dce6;
  }
</style>