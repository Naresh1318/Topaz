<template>
  <div class="home">
    <nav-bar active_page="Home"></nav-bar>
    <v-content>
      <div class="pa-3">
        <project-card :title="projects[0].title" :url="projects[0].url"
        :description="projects[0].description" :stars="projects[0].stars"
        :primary_language="projects[0].primary_language"
        :primary_language_color="projects[0].primary_language_color"
        :image_url="projects[0].image_url"></project-card>
      </div>
    </v-content>
  </div>
</template>

<script>
import NavBar from '../components/NavBar.vue';
import ProjectCard from '../components/ProjectCard.vue';

export default {
  name: 'Home',
  data() {
    return {
      page_name: 'Home',
      projects: [
        {
          title: 'Topaz',
          url: 'https://github.com/Naresh1318/Topaz',
          description: 'Test text goes here cause it\'s a test',
          primary_language: 'lol',
          primary_language_color: '#123456',
          stars: 1000,
          image_url: 'https://raw.githubusercontent.com/Naresh1318/Dopamine/master/resources/icons/icon.png',
        },
      ],
    };
  },
  components: {
    navBar: NavBar,
    projectCard: ProjectCard,
  },
};
</script>
