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
        <v-row no-gutters>
          <v-col cols="3">
            <v-row>
              <v-col cols="1">
                <span class="dot"
                      :style="{'background-color': primary_language_color}">
                </span>
              </v-col>
              <v-col cols="8" class="hide-overflow">
                {{primary_language}}
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="4">
            <v-row>
              <v-col cols="2">
                <v-icon style="font-size: 20px; margin-bottom: 1px; margin-bottom: 3px">
                  fa-star
                </v-icon>
              </v-col>
              <v-col cols="8">
                {{ stars }}
              </v-col>
            </v-row>
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
  name: 'ProjectCard',
  props: {
    title: String,
    url: String,
    description: String,
    primary_language: String,
    primary_language_color: String,
    stars: String,
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
}

a:hover {
  text-decoration: underline;
}

.hide-overflow {
    text-overflow: ellipsis;
    overflow: hidden;
    white-space: nowrap;
}

.dot {
  height: 15px;
  width: 15px;
  border-radius: 50%;
  display: inline-block;
}
</style>
