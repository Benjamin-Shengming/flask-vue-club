import Vue from 'vue'
import Router from 'vue-router'
const routerOptions = [
  { path: '/:club_name', component: 'Home' },
  { path: '/:club_name/about', component: 'About' },
  { path: '/:club_name/service/:service_id/edit', component: 'ServiceEdit' },
  { path: '*', component: 'NotFound' }
]
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})
Vue.use(Router)
export default new Router({
  routes,
  mode: 'history'
})
