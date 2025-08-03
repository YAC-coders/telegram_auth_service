<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md" style="max-width: 400px">

      <q-form @submit="onSubmit" @reset="onReset" class="q-gutter-md">
        <IntlTelInput v-model="phoneNumber" :options="{
          initialCountry: 'ru',
        }" />
        <div>
          <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
          <q-btn label="Submit" type="submit" color="primary" />
        </div>
      </q-form>

    </div>
  </q-page>
</template>

<script setup>
import IntlTelInput from "intl-tel-input/vueWithUtils"
import "intl-tel-input/styles"
import { ref } from "vue"

const phoneNumber = ref('')

const onSubmit = () => {
  console.log(phoneNumber.value)
}

const onReset = () => {
  phoneNumber.value = ''
}
</script>
