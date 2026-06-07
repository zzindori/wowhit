import { initializeApp, getApps } from 'firebase/app'
import { getFirestore } from 'firebase/firestore'

const firebaseConfig = {
  apiKey: 'AIzaSyBKLQE8WF-HciO_2HyocztSKxKy5PxAXLI',
  authDomain: 'itneapp.firebaseapp.com',
  projectId: 'itneapp',
  storageBucket: 'itneapp.firebasestorage.app',
  messagingSenderId: '231435424889',
  appId: '1:231435424889:web:e6b37b8cb3d070eea330a8',
}

export default defineNuxtPlugin(() => {
  const app = getApps().length ? getApps()[0]! : initializeApp(firebaseConfig)
  const db = getFirestore(app)
  return { provide: { db } }
})
