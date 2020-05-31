<template>
  <div>
    <v-container class="centered">
      <v-card style="margin: auto; padding: 2rem" :max-width="card_width()">
        <v-row>
          <v-col xl="3">
            <h1>Topaz</h1>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col xl="10">
            <v-text-field v-model="username" label="Name" required color="dark"></v-text-field>
          </v-col>
        </v-row>
        <v-row justify="center">
          <v-col xl="10">
            <v-text-field v-model="password" type="password" label="Password"
                          required color="dark"></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col xl="3">
            <v-btn @click="login()" color="dark" dark>Login</v-btn>
          </v-col>
        </v-row>
      </v-card>
    </v-container>
  <v-snackbar v-model="show_alert">
      Wrong username or password <v-btn color="#fff" text @click="show_alert=false">Close</v-btn>
  </v-snackbar>
  </div>
</template>

<script>
export default {
  data() {
    return {
      name: 'Login',
      show_alert: false,
      username: '',
      password: '',
    };
  },
  methods: {
    login() {
      this.$http.post(`${this.$backend_address}/login_user`, {
        username: this.username,
        password: this.password,
      },
      {
        withCredentials: true,
      })
        .then((response) => {
          if (!response.data.logged_in) {
            this.username = '';
            this.password = '';
            this.show_alert = true;
          } else {
            this.$router.push('/');
          }
        });
    },
    is_mobile() {
      if (/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
        return true;
      }
      return false;
    },
    card_width() {
      if (this.is_mobile()) {
        return '90%';
      }
      return '40%';
    },
  },
};
</script>

<style scoped>
.centered {
  position: fixed;
  top: 50%;
  left: 50%;
  /* bring your own prefixes */
  transform: translate(-50%, -50%);
}
</style>
