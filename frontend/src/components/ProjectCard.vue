<template>
  <v-container style="position: relative">
    <v-row>
      <v-col cols="8">
        <v-row>
          <v-col>
            <a :href="url">{{ title }}</a>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <p class="hide-overflow">{{ description }}</p>
          </v-col>
        </v-row>
        <v-row style="position: absolute; bottom: 5px">
          <v-col cols="6">
            <v-row no-gutters>
              <v-col>
                <v-row no-gutters>
                  <v-col>
                    <span class="dot"
                          :style="{'background-color': primary_language_color}">
                    </span>
                  </v-col>
                  <v-col>
                    {{primary_language}}
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-col>
          <v-col cols="6">
            <v-row no-gutters>
              <v-col>
                <v-row no-gutters>
                  <v-col cols="6">
                    <v-icon>fa-star</v-icon>
                  </v-col>
                  <v-col cols="6">
                    {{ stars }}
                  </v-col>
                </v-row>
              </v-col>
            </v-row>
          </v-col>
        </v-row>
      </v-col>
      <v-col cols="4">
        <v-img height="200px" :src="image_url" contain></v-img>
      </v-col>
    </v-row>
    <v-divider></v-divider>
  </v-container>
</template>

<script>
export default {
  name: 'ProjectCard',
  props: ['title', 'url', 'description', 'primary_language', 'primary_language_color', 'stars', 'image_url'],
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
  text-align: center;
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
