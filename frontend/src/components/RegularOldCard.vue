<template>
  <v-container>
    <v-row>
      <v-col md="8" sm="12" order-md="1" order-sm="12">
        <v-row>
          <v-col>
            <a v-if="!name" :href="url">{{ title }}</a>
            <a v-else @click="navigate_to_blog(name, file_type)">{{ title }}</a>
          </v-col>
        </v-row>
        <v-row style="height: 50%">
          <v-col>
            <p>{{ description }}</p>
          </v-col>
        </v-row>
      </v-col>
      <v-col md="4" sm="12" order-md="2" order-sm="1">
        <v-card elevation="5" style="border-radius: 5px;">
          <v-img height="175px" :src="image_url"></v-img>
        </v-card>
      </v-col>
    </v-row>
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
    name: String,
    file_type: Number,
  },
  data() {
    return {
    };
  },
  methods: {
    navigate_to_blog(name, fileType) {
      this.$router.push(`/blog/post?page=${name}&file_type=${fileType}`);
    },
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
