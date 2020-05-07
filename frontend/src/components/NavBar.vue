<template>
  <div>
    <v-navigation-drawer
      class="nav_bar"
      app
      width="300"
    >
      <v-card
        class="nav_bar_card"
        dark
        color="#101010"
        raised
        height="100%"
      >
        <v-container
          style="height: 90vh"
        >
          <v-row align="center" style="height: 100%">
            <v-col>
              <v-row>
                <v-col>
                  <a class="btn-text">Home</a>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <a class="btn-text">Projects</a>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <a class="btn-text">Blog</a>
                </v-col>
              </v-row>
              <v-row>
                <v-col>
                  <a class="btn-text">About me</a>
                </v-col>
              </v-row>
            </v-col>
          </v-row>
        </v-container>

        <!-- Navigation footer -->
        <v-container style="bottom: 0; position: absolute">
          <v-row>
            <v-col cols="12" style="text-align: center">
              <div style="font-family: 'Beth Ellen', sans-serif">
                Naresh Nagabushan
              </div>
            </v-col>
          </v-row>
          <v-row justify="center">
            <v-col cols="2" style="text-align: center">
              <a href="" style="text-decoration: none">
                <v-icon>fa-github</v-icon>
              </a>
            </v-col>
            <v-col cols="2" style="text-align: center">
              <a href="" style="text-decoration: none">
                <v-icon>fa-medium</v-icon>
              </a>
            </v-col>
            <v-col cols="2" style="text-align: center">
              <a href="" style="text-decoration: none">
                <v-icon>fa-linkedin</v-icon>
              </a>
            </v-col>
            <v-col cols="2" style="text-align: center">
              <a href="" style="text-decoration: none">
                <v-icon>fa-twitter</v-icon>
              </a>
            </v-col>
          </v-row>
        </v-container>
      </v-card>
    </v-navigation-drawer>
  </div>
</template>

<script>
export default {
  name: 'NavBar',
  props: ['text'],
  data() {
    return {
    };
  },
};
</script>

<style scoped>
.nav_bar {
  font-family: 'Source Sans Pro', sans-serif !important;
}

.nav_bar_card {
  border-radius: 0 !important;
}

.btn-text {
  font-family: 'Source Sans Pro', sans-serif;
  position: relative;
  display: inline-block;
  font-size: 24px;
  font-weight: 400;
  text-align: center;
  color: #fff;
  padding: 0.75rem;
}

.btn-text:hover {
  cursor: pointer;
  text-decoration: underline;
}
</style>
