<script setup lang="ts">
definePageMeta({ middleware: 'auth' })

const { login, isAuthenticated } = useAuth()

const form = reactive({
  username: '',
  password: ''
})

const error = ref('')
const isSubmitting = ref(false)

onMounted(() => {
  if (isAuthenticated.value) {
    navigateTo('/consultations')
  }
})

const submit = async () => {
  if (!form.username.trim() || !form.password.trim()) {
    error.value = 'Please enter your username and password.'
    return
  }

  isSubmitting.value = true
  error.value = ''

  try {
    await login({
      username: form.username.trim(),
      password: form.password
    })

    await navigateTo('/consultations')
  } catch (err) {
    error.value = err instanceof Error ? err.message : 'Unable to sign in. Please try again.'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-brand">
        <div class="brand-mark">CC</div>
        <div>
          <strong>ClinicCare</strong>
          <span>Mini EMR</span>
        </div>
      </div>

      <div class="auth-copy">
        <h1>Welcome back</h1>
        <p>Sign in to continue with patient consultations and clinical records.</p>
      </div>

      <form class="auth-form" @submit.prevent="submit">
        <div class="field-group">
          <label for="username">Username</label>
          <input id="username" v-model="form.username" class="form-control" type="text" autocomplete="username" placeholder="doctor01" />
        </div>

        <div class="field-group">
          <label for="password">Password</label>
          <input id="password" v-model="form.password" class="form-control" type="password" autocomplete="current-password" placeholder="Enter password" />
        </div>

        <div v-if="error" class="form-message form-message--error">{{ error }}</div>

        <button class="primary-button" type="submit" :disabled="isSubmitting">
          {{ isSubmitting ? 'Signing in…' : 'Sign in' }}
        </button>
      </form>
    </div>
  </div>
</template>
