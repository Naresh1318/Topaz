<template>
  <div class="add_external_link_card">
    <v-card>
      <v-card-title>Add blog from other sources</v-card-title>
      <v-card-text>
        <v-row>
          <v-col>
            <v-text-field v-model="title" label="Title" required color="dark"></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-textarea v-model="description" label="Description"
                        required color="dark"></v-textarea>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-text-field v-model="url" label="URL" required color="dark"></v-text-field>
          </v-col>
          <v-col>
            <v-text-field v-model="image_url" label="Image URL"
                          required color="dark"></v-text-field>

          </v-col>
        </v-row>
        <v-row>
          <v-col cols="6">
            <v-text-field v-model="time_stamp" label="Label Text" type="date" required
                          color="dark"></v-text-field>
          </v-col>
        </v-row>
        <v-row>
          <v-col>
            <v-btn @click="submit_entry()" color="dark" dark>Submit</v-btn>
          </v-col>
        </v-row>
      </v-card-text>
    </v-card>
    <v-snackbar v-model="show_alert"> {{ alert_text }}
      <v-btn color="#fff" text @click="show_alert=false">Close</v-btn>
    </v-snackbar>
  </div>
</template>

<script>
export default {
  name: 'AddExternalBlogLinks',
  data() {
    return {
      title: '',
      description: '',
      url: '',
      image_url: '',
      time_stamp: '',
      show_alert: false,
      alert_text: '',
    };
  },
  methods: {
    /**
     * Try submitting entry
     */
    submit_entry() {
      if (this.title === '' || this.description === '' || this.url === '' || this.image_url === ''
        || this.time_stamp === '') {
        this.alert_text = 'Fill all entries';
        this.show_alert = true;
        return;
      }
      this.$http.post(`${this.$backend_address}/blogs/external_link`, {
        title: this.title,
        description: this.description,
        url: this.url,
        image_url: this.image_url,
        time_stamp: this.time_stamp,
      }, {
        withCredentials: true,
      })
        .then((response) => {
          if (response.data.INFO) {
            this.alert_text = response.data.INFO;
            this.show_alert = true;
            this.$emit('submitted', true);
          }
        });
    },
  },
};
</script>

<style scoped>
.add_external_link_card {
  width: 70%;
}
</style>
