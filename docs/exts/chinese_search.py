from sphinx.search import SearchLanguage
import jieba

class SearchChinese(SearchLanguage):
    lang = 'zh'

    def init(self, options):
        pass

    def split(self, input):
        return jieba.cut_for_search(input.encode("utf8")) 

    def word_filter(self, stemmed_word):
        return True

def setup(app): 
    import sphinx.search as search
    search.languages["zh_CN"] = SearchChinese
