<template>
  <v-container>
    <v-row>
      <v-col md="8" xs="12">
        <v-row>
          <v-col cols="12" class="hide-overflow">
            <a :href="url">{{ title }}</a>
          </v-col>
        </v-row>
        <v-row>
          <v-col cols="12">
            <p>{{ description }}</p>
          </v-col>
        </v-row>
        <v-row v-if="is_mobile && image_url !== ''">
          <v-col>
            <v-img height="175px" :src="image_url" contain style="min-width: 100%"></v-img>
          </v-col>
        </v-row>
        <v-row no-gutters>
          <v-col md="3" xs="6">
            <v-row>
              <v-col cols="1">
                <span class="dot"
                      :style="{'background-color': primary_language_color}">
                </span>
              </v-col>
              <v-col md="8" xs="6" class="hide-overflow">
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
      <v-col v-if="!is_mobile && image_url !== ''" md="4" xs="12">
        <v-img height="175px" :src="image_url" contain style="min-width: 100%"></v-img>
      </v-col>
    </v-row>
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
    is_mobile: Boolean,
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
