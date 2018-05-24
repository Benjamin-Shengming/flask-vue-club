<template>
  <b-container fluid>
    <b-row class="email_tel" >
        <b-col sm="3">
            <label> Email or Tel </label>
        </b-col>
        <b-col sm="9">
            <b-form-input id="email_tel_input">
            </b-form-input>
        </b-col>
    </b-row>
    <b-row class="user-password" >
        <b-col sm="3">
            <label> password</label>
        </b-col>
        <b-col sm="9">
            <b-form-input id="user_password_input" type='password'>
            </b-form-input>
        </b-col>
    </b-row>
  </b-container>
</template>

<script>
export default {
  data () {
    return {
    }
  }
}
</script>
