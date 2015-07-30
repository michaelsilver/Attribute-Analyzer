import unittest
from wikimap import wikimap
import networkx.testing as nxt


class TestGeneralNetworkMethods(unittest.TestCase):

    def setUp(self):
        self.G = wikimap.WikiMap()

        # four node group
        self.G.add_edge("A", "B")
        self.G.add_edge("A", "C")
        self.G.add_edge("D", "C")

        # three node group
        self.G.add_edge("Y", "X")
        self.G.add_edge("Z", "X")

        # three node group (another)
        self.G.add_edge("alpha", "beta")
        self.G.add_edge("alpha", "gamma")

        # two node group
        self.G.add_edge("M", "N")

    def test_connected_component_lengths(self):
        self.assertItemsEqual(self.G.connected_component_lengths(), [2, 3, 3, 4])

    def test_connected_component_statistics(self):
        self.assertEqual(self.G.connected_component_statistics(), {2:1, 3:2, 4:1})

    @unittest.expectedFailure
    def test_connected_components_with_size(self):
        # three node group
        expected_three1 = wikimap.WikiMap()
        expected_three1.add_edge("Y", "X")
        expected_three1.add_edge("Z", "X")

        # three node group (another)
        expected_three2 = wikimap.WikiMap()
        expected_three2.add_edge("alpha", "beta")
        expected_three2.add_edge("alpha", "gamma")

        # four node group
        expected_four = wikimap.WikiMap()
        expected_four.add_edge("A", "B")
        expected_four.add_edge("A", "C")
        expected_four.add_edge("D", "C")

        self.assertEqual(len(self.G.connected_components_with_size(3)),
                              len([expected_three1, expected_three2]))
        # unfortunately cannot test that two lists of graphs are
        # equal, so only test length of lists here, and then that the
        # graph in the list of len=1 below is equal. Hopefully this is
        # enough.

        returned_four = self.G.connected_components_with_size(4)[0]
        nxt.assert_graphs_equal(returned_four, expected_four)


class TestCleaningNodes(unittest.TestCase): 
    def test_clean_skips(self):
        self.assertEqual(wikimap.WikiMap.clean("File: foo"), "File: foo")
        self.assertEqual(wikimap.WikiMap.clean("!!!!!foo!!!!!"), "!!!!!foo!!!!!")

    def test_clean_unicode(self):
        self.assertEqual(wikimap.WikiMap.clean(u'Rate\xa0of\xa0fire'), "rate of fire")

    def test_clean_punct_remove(self):
        # capitalization and punctuation removal
        self.assertEqual(wikimap.WikiMap.clean("Heights"), "heights")
        self.assertEqual(wikimap.WikiMap.clean("discovery_site"), "discovery site")
        self.assertEqual(wikimap.WikiMap.clean("Max. devices"), "max devices")
        self.assertEqual(wikimap.WikiMap.clean("Circus tent?"), "circus tent")
        self.assertEqual(wikimap.WikiMap.clean("Web site:"), "web site")
        self.assertEqual(wikimap.WikiMap.clean("/Karaoke"), "karaoke")

    def test_clean_punct_except(self):
        # exception to punctuation removal
        self.assertEqual(wikimap.WikiMap.clean("% of total exports"),
                         "% of total exports")
        self.assertEqual(wikimap.WikiMap.clean("Managing editor, design"),
                         "managing editor, design")
        self.assertEqual(wikimap.WikiMap.clean("MSRP US$"), "msrp us$")
        self.assertEqual(wikimap.WikiMap.clean("Specific traits & abilities"),
                         "specific traits & abilities")
        self.assertEqual(wikimap.WikiMap.clean("re-issuing"), "re-issuing")
        # another good example: "Capital-in-exile"

    def test_clean_HTML_remove(self):
        # HTML-like junk removal
        self.assertEqual(wikimap.WikiMap.clean("<hiero>G16</hiero>"), "g16")
        self.assertEqual(wikimap.WikiMap.clean("&mdot;foo"), "foo")
        self.assertEqual(wikimap.WikiMap.clean("Opened</th>"), "opened")

    def test_clean_parens(self):
        self.assertEqual(wikimap.WikiMap.clean("Parent club(s)"), "parent club")
        self.assertEqual(wikimap.WikiMap.clean("Team president (men)"), "team president")
        self.assertEqual(wikimap.WikiMap.clean("Deaconess(es)"), "deaconess")
        self.assertEqual(wikimap.WikiMap.clean("ARWU[5]"), "arwu")

    def test_clean_possessive(self):
        self.assertEqual(wikimap.WikiMap.clean("Women's coach"), "women's coach")
        self.assertEqual(wikimap.WikiMap.clean("Teams' champion"), "teams' champion")

class TestAddToField(unittest.TestCase):
    def setUp(self):
        self.test_dict = ["bannana", {"foo": ["bar"]}]

    def test_add_to_existing_field_new(self):
        wikimap.WikiMap.add_to_field(self.test_dict[1], "foo", "aba")
        self.assertEqual(self.test_dict[1], {"foo": ["bar", "aba"]})

    def test_add_to_existing_field_existing(self):
        wikimap.WikiMap.add_to_field(self.test_dict[1], "foo", "bar")
        self.assertEqual(self.test_dict[1], {"foo": ["bar"]})

    def test_add_to_new_field(self):
        wikimap.WikiMap.add_to_field(self.test_dict[1], "bar", "aba")
        self.assertEqual(self.test_dict[1], {"foo": ["bar"], "bar": ["aba"]})


# class TestInsertingInformation(unittest.TestCase):

#     def setUp(self):
#         self.G = wikimap.WikiMap()

#     def test_add_to_field(self):
#         # stub

#     def test_add_uncleaned(self):
#         # stub

#     def test_add_rendering(self):
#         # stub

#     def test_add_infobox(self):
#         # stub

#     def test_add_mapping(self):
#         # stub

# class TestFetchingInformation(unittest.TestCase):

#     def setUp(self):
        

#     def test_infoboxes_of_graph_node(self):
#         # stub

#     def test_infoboxes_of_graph(self):
#         # stub

#     def test_rendering_of_graph_node(self):
#         # stub
