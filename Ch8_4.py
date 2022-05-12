import datetime
from newsmth_pg import NewsmthCrawl

class TestClass():
  def test_lastreplydatesort(self):
    Nsc = NewsmthCrawl()
    Nsc.set_startpage(3)
    Nsc.set_maxpage(10)
    tup_list = Nsc.get_all_items()
    for i in range(1, len(tup_list)):
      dt_new = datetime.datetime.strptime(tup_list[i-1][-1], '%Y-%m-%d')
      dt_old = datetime.datetime.strptime(tup_list[i][-1], '%Y-%m-%d')
      assert dt_new >= dt_old
