const app = {
    data() {
        return {
            usuario: '',
            correo: '',
            clave: '',
            nombre: 'chang'
        }
    },
    methods: {
        llamarSaludoDesdeHijo(){
            this.$refs.menuComponent.saludarDesdeHijo(this.nombre);
        }
    }
}

const _app = Vue.createApp(app);
