const TranslationEditor = {
  props: ["source", "trans", "current_value"],
  data () {
      return {
          uploading_data: false,
          edit_mode: false,
          editable_value: ""
      }
  },
  methods: {
      startEditing() {
        this.edit_mode = true;
      },
      saveTranslation() {
          if (this.uploading_data) return false;
          this.uploading_data = true;
          data = {
              source_id: this.source.id,
              lang: this.trans.lang,
              value: this.trans.value
          };
          fetch("/suggest-translation/", {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'same-origin',
            headers: {
              'Content-Type': 'application/json'
            },
            redirect: 'follow',
            referrerPolicy: 'no-referrer',
            body: JSON.stringify(data) //
          }).then(response => response.json())
            .then(info => {
                this.uploading_data = false;
                this.edit_mode=false;
                console.log(info)
            })
      }
  },
  template: `
    <div class="translation-editor">
        <i class="flag" :class="'flag-'+trans.lang"/>
        <div v-if="edit_mode" class="te-content edit-mode">
            <textarea width="100%" v-model="trans.value" class="form-control edit-area"></textarea>
            <input type="button" value="save" class="btn btn-primary"  v-on:click="saveTranslation()" />
            <input type="button" value="cancel" class="btn btn-danger" v-on:click="edit_mode=false" />
        </div>
        <div v-else class="te-content view-mode">
            <a title="Suggest new translation" v-on:click.prevent="startEditing()" class="edit-button">
                <i class="fa fa-edit"></i>
                <span>{{ trans.value }}</span>
            </a>
        </div>
    </div>
  `
};

const SourcesList = {
  data() {
    return {
        is_loading: true,
        langs: [],
        sources: [],
        search_term: "",
        current_lang: "all"
    }
  },
  methods: {
      isLangNeeded(lang) {
          const cur_lang = this.current_lang;
          if ( ! cur_lang || cur_lang === "all") return true;
          return cur_lang === lang;
      },
      getTransForLang(source, lang) {
          for (let trans of source.translations) {
              if (trans.lang === lang) return trans.value;
          }
          return ""
      },
      getTrans(source) {
          let showTrans = [];
          this.langs.forEach(
              (val) => {
                  showTrans.push({
                      "lang": val.code,
                      "value": this.getTransForLang(source, val.code)
                  })
              }
          );
          return showTrans;
      }
  },
  computed: {
    sourcesComputed()  {
        let sources = this.sources;
        if (this.search_term) {
            sources = sources.filter((s) => s.value.toLowerCase().indexOf(this.search_term.toLowerCase()) !== -1)
        }
        return sources
    }
  },
  mounted () {
    fetch("/get-translations-info/")
        .then(response => response.json())
        .then(info => {this.langs = info.langs; this.sources=info.sources; this.is_loading=false})
  },
  template: `
    <h2 v-if="is_loading">Data is loading. Please wait...</h2>
    <div class="main-container" v-else>
        <div class="translations-toolbox">
            <form class="form-inline" autocomplete="off">
              <label class="sr-only" for="search">Search</label>
              <div class="input-group mb-2 mr-sm-2">
                <input type="text" class="form-control" name="q" id="search" placeholder="Search" v-model="search_term">
              </div>

              <div class="form-check mb-2 mr-sm-2">
                <select name="lang" class="form-control" v-model="current_lang">
                    <option value="all">all</option>
                    <option v-for="lang in langs" :value="lang.code">{{ lang.title }}</option>
                </select>
              </div>
            </form>
        </div>

        <table class="table">
            <thead>
                <tr>
                    <th width="20%">src</th>
                    <th>i18n</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="source in sourcesComputed">
                    <td>{{ source.value }}</td>
                    <td>
                        <div class="translations-list">
                            <TranslationEditor :source="source" :trans="trans" v-for="trans in getTrans(source)" v-show="isLangNeeded(trans.lang)" />   
                        </div>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
  `
};

const app = Vue.createApp(SourcesList);
app.component('TranslationEditor', TranslationEditor);
app.mount("#translations-list-app");