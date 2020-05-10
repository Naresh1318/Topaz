<template>
  <v-container>
    <v-row>
      <v-col cols="8">
        <v-row>
          <v-col>
            <a :href="url">{{ title }}</a>
          </v-col>
        </v-row>
        <v-row style="height: 50%">
          <v-col>
            <p>{{ description }}</p>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="4">
        <v-img height="175px" :src="image_url" contain></v-img>
      </v-col>
    </v-row>
    <v-divider></v-divider>
  </v-container>
</template>

<script>
export default {
  name: 'RegularOldCard',
  props: {
    title: String,
    url: String,
    description: String,
    image_url: String,
  },
  data() {
    return {
    };
  },
};
</script>

<style scoped>
a {
  position: relative;
  display: inline-block;
  font-size: 24px;
  font-weight: 500;
  color: #000 !important;
  text-decoration: none;
  text-align: left;
}

a:hover {
  text-decoration: underline;
}
</style>
