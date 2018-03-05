<template>
  <div>
    <div> <!-- nav bar -->
      <b-navbar toggleable="md" type="dark" variant="info">
        <b-navbar-toggle target="nav_collapse"></b-navbar-toggle>
        <b-navbar-brand :href="url_home">{{ clubName }}</b-navbar-brand>
        <b-collapse is-nav id="nav_collapse">
          <b-navbar-nav>
            <b-nav-item :href="url_home">首页</b-nav-item>
            <b-nav-item-dropdown right>
              <!-- Using button-content slot -->
              <template slot="button-content">
                <em>产品服务</em>
              </template>
              <b-dropdown-item v-on:click="createService">新增服务产品</b-dropdown-item>
              <b-dropdown-item v-on:click="showServices">查看服务产品</b-dropdown-item>
            </b-nav-item-dropdown>

            <b-nav-item v-on:click="showUsers">用户</b-nav-item>
          </b-navbar-nav>

          <!-- Right aligned nav items -->
          <b-navbar-nav class="ml-auto">
            <b-container fluid>
              <b-nav-item v-on:click="createService">新服务产品</b-nav-item>
            </b-container>
          </b-navbar-nav>
        </b-collapse>
      </b-navbar>
    </div>

  <!-- service create button-->
  <div> 
  </div>

  <!-- services manage button-->
  <div v-if="serviceNew"> 
    <b-container fluid>
      <ServiceNew @event-service-created="showServices"> </ServiceNew>
    </b-container>
  </div>

  <!-- service view page -->
  <div v-if="serviceView">
    <b-container fluid>
      <ServiceListEdit @event-service-delete="deleteService" :msg='item'
                       @event-service-modify="modifyService"  > 
      </ServiceListEdit>
    </b-container>
  </div>

  <!-- single service edit -->
  <div v-if="serviceEdit">
    <b-container fluid>
      <ServiceEdit :service="singleService" > 
      </ServiceEdit>
    </b-container>
  </div>

  <!-- user manage page -->
  <div v-if="userView"> 
    <b-container fluid>
      <p> this is user page</p>
    </b-container>
  </div>
  </div>

</template>

<script>
import ServiceNew from "./ServiceNew.vue"
import ServiceListEdit from "./ServiceListEdit.vue"
import ServiceEdit from "./ServiceEdit.vue"
export default {
  components: {
    ServiceNew,
    ServiceListEdit,
    ServiceEdit
  },
  data() {
    return {
      serviceView: true,
      serviceNew: false,
      serviceEdit: false,
      userView: false,

      // editing service
      singleService: null
    };
  },
  computed: {
    majorImg: {
      get: function() {
        return this.majorImgFile;
      },
      set: function(newvalue) {
        this.majorImgFile = newvalue;
        this.previewMajorImg();
      }
    },
    clubName: function() {
      return this.$route.params.club_name;
    },
    url_home: function() {
      return "/" + this.clubName;
    }
  },
  methods: {
    deleteService(item) {
      console.log(item)
    },
    modifyService(item) {
      console.log("need to modify")
      console.log(item)
      this.singleService = item;
      this.serviceView = false;

      this.serviceNew = false;
      this.userView = false;
      this.serviceEdit = true;
    },
    showServices() {
      this.serviceView = true;

      this.serviceNew = false;
      this.userView = false;
      this.serviceEdit = false;
    },
    createService() {
      this.serviceView = false;
      this.serviceNew = true;
      this.userView = false;
      this.serviceEdit = false;
    },
    showUsers() {
      this.serviceNew = false;
      this.serviceView = false;
      this.userView = true;
    }
  },
  mounted () {
    console.log("mounted was called");
  },
  created() {
    console.log("created was called");
  }
};
</script>