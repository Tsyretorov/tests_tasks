<template>
  <div>
    <DatePicker v-if="step === 1" @next="handleDateSelect" />

    <UserData
      v-if="step === 2"
      :selectedDate="selectedDate"
      :user="user"
      @share="handleShare"
    />

    <ShareData v-if="step === 3" :shareLink="shareLink" @back="handleBack" />

    <div v-if="step === 4">
      <h1>Данные пользователя</h1>
      <p>Дата: {{ selectedDate }}</p>
      <p>Имя: {{ user.firstName }}</p>
      <p>Фамилия: {{ user.lastName }}</p>
      <p>Username: {{ user.username }}</p>
    </div>

    <div v-if="step === 0">
      <h1>Error</h1>
      <p>Здесь ничего нет, потому что ты не через бота, да и ссылка видимо не та :\ @Poni_Ponibot</p>
    </div>
  </div>
</template>

<script>
import DatePicker from "./components/DatePicker.vue";
import UserData from "./components/BirthdayCountdown.vue";
import ShareData from "./components/BirthdayCountdownShared.vue";
import axios from 'axios';

export default {
  components: {
    DatePicker,
    UserData,
    ShareData,
  },
  data() {
    return {
      step: 1,
      selectedDate: null,
      user: null,
      shareLink: null,
    };
  },
  mounted() {
    const urlParams = new URLSearchParams(window.location.search);

    if (urlParams.has("username")) {
      const username = urlParams.get("username");
      this.fetchSharedUserData(username);
      this.step = 4;
    } else {
      const tg = window.Telegram.WebApp;
      if (tg.initDataUnsafe.user) {
        this.user = {
          firstName: tg.initDataUnsafe.user.first_name || "Не указано",
          lastName: tg.initDataUnsafe.user.last_name || "Не указано",
          username: tg.initDataUnsafe.user.user_name || "Не указано",
        };
      } else {
        this.step = 1;
      }
    }
  },

  methods: {
    async fetchSharedUserData(username) {
      try {
        const response = await axios.get(`/api/user/${username}/birthday`);
        this.user = {
          firstName: response.data.firstName,
          lastName: response.data.lastName,
          username: response.data.username,
        };
        this.selectedDate = response.data.birth_date;
      } catch (error) {
        console.error("Ошибка при получении данных:", error);
      }
    },

    async handleDateSelect(date) {
      console.log(date)
      this.selectedDate = date;

      const tg = window.Telegram.WebApp;
      if (tg.initDataUnsafe.user) {
        const formattedDate = new Date(this.selectedDate).toISOString().split('T')[0];
        const userData = {
          telegram_id: tg.initDataUnsafe.user.id,
          firstName: tg.initDataUnsafe.user.first_name || "Не указано",
          lastName: tg.initDataUnsafe.user.last_name || "Не указано",
          username: tg.initDataUnsafe.user.user_name || "Не указано",
          birth_date: formattedDate,
        };
        console.log("DATE", userData)
        try {
          console.log(userData)
          const response = await axios.post("/api/user/", userData);
          this.user = userData;
          this.step = 2;
        } catch (error) {
          console.error("Ошибка при сохранении данных:", error.response.data);
        }
      } else {
        const formattedDate = new Date(this.selectedDate).toISOString().split('T')[0];
        console.log(formattedDate)
        const userData = {
          telegram_id: 123,
          firstName: "без теграмма Не указано",
          lastName: "без теграмма Не указано",
          username: "без теграмма Не указано",
          birth_date: formattedDate,
        };
        console.log("DATE", userData)
        try {
          const response = await axios.post("/api/user/", userData);
          console.log(response)
          this.user = userData;
          this.step = 2;
        } catch (error) {
          console.error("Ошибка при сохранении данных:", error.response.data);
        }
      }
    },

    async fetchUserData() {
      const tg = window.Telegram.WebApp;
      if (tg.initDataUnsafe.user) {
        const username = tg.initDataUnsafe.user.username;
        try {
          const response = await axios.get(`/api/user/${username}/birthday`);
          this.user = {
            firstName: response.data.first_name,
            lastName: response.data.last_name,
            username: response.data.username
          };
          this.selectedDate = {
            days_until_birthday: response.data.days_until_birthday,
            hours_until_birthday: response.data.hours_until_birthday,
            minutes_until_birthday: response.data.minutes_until_birthday,
          }
        } catch (error) {
          console.error("Ошибка при получении данных:", error);
        }
      }
    },

    handleShare() {
      const baseUrl = window.location.origin + window.location.pathname;
      const queryParams = new URLSearchParams({
        username: this.user.username,
      }).toString();

      this.shareLink = `${baseUrl}?${queryParams}`;

      navigator.clipboard.writeText(this.shareLink).then(() => {
        alert("Ссылка скопирована в буфер обмена!");
      });

      this.step = 3;
    },

    handleBack() {
      this.step = 2;
    },
  },
};
</script>