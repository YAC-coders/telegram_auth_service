<template>
  <q-page class="flex flex-center">
    <div class="q-pa-md" style="max-width: 400px">
      <q-form
      @submit="onSubmit"
      @reset="onReset"
      class="q-gutter-md"
    >
      <q-input
        filled
        v-model="phoneNumber"
        type="tel"
        label="Your phone *"
        hint="Enter your telephone number"
        lazy-rules
        :rules="[ val => val && val.length > 0 || 'Please type phone number']"
      />



      <div>
        <q-btn label="Reset" type="reset" color="primary" flat class="q-ml-sm" />
        <q-btn label="Submit" type="submit" color="primary"/>
      </div>
    </q-form>

    </div>
  </q-page>
</template>

<script setup>
//
</script>
