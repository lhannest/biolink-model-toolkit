import pytest

from bmt import Toolkit


@pytest.fixture(scope="module")
def toolkit():
    return Toolkit()


def test_get_all_elements(toolkit):
    elements = toolkit.get_all_elements()
    assert 'named thing' in elements
    assert 'association' in elements
    assert 'related to' in elements
    assert 'uriorcurie' in elements

    elements = toolkit.get_all_elements(formatted=True)
    assert 'biolink:NamedThing' in elements
    assert 'biolink:GeneToGeneAssociation' in elements
    assert 'biolink:related_to' in elements
    assert 'metatype:Uriorcurie' in elements
    assert 'biolink:Frequency' in elements


def test_get_all_entities(toolkit):
    entities = toolkit.get_all_entities()
    assert 'named thing' in entities
    assert 'gene' in entities
    assert 'disease' in entities
    assert 'association' not in entities
    assert 'related to' not in entities

    entities = toolkit.get_all_entities(formatted=True)
    assert 'biolink:NamedThing' in entities
    assert 'biolink:Gene' in entities
    assert 'biolink:Disease' in entities


def test_get_all_associations(toolkit):
    associations = toolkit.get_all_associations()
    assert 'association' in associations
    assert 'gene to gene association' in associations
    assert 'named thing' not in associations

    associations = toolkit.get_all_associations(formatted=True)
    assert 'biolink:Association' in associations
    assert 'biolink:GeneToGeneAssociation' in associations


def test_get_all_node_properties(toolkit):
    properties = toolkit.get_all_node_properties()
    assert 'name' in properties
    assert 'category' in properties
    assert 'has gene' in properties

    properties = toolkit.get_all_node_properties(formatted=True)
    assert 'biolink:name' in properties
    assert 'biolink:category' in properties
    assert 'biolink:has_gene' in properties


def test_get_all_edge_properties(toolkit):
    properties = toolkit.get_all_edge_properties()
    assert 'subject' in properties
    assert 'object' in properties
    assert 'frequency qualifier' in properties

    properties = toolkit.get_all_edge_properties(formatted=True)
    assert 'biolink:subject' in properties
    assert 'biolink:object' in properties
    assert 'biolink:frequency_qualifier' in properties


def test_get_element(toolkit):
    gene = toolkit.get_element('gene')
    locus = toolkit.get_element('locus')
    assert gene == locus

    o = toolkit.get_element('drug intake')
    assert o and o.name == 'drug exposure'

    o = toolkit.get_element('molecular function')
    assert o and o.name == 'molecular activity'

    o = toolkit.get_element('RNA Product')
    assert o and o.name == 'RNA product'

    o = toolkit.get_element('rna product')
    assert o and o.name == 'RNA product'


def test_predicate(toolkit):
    assert not toolkit.is_predicate('named thing')
    assert not toolkit.is_predicate('gene')
    assert toolkit.is_predicate('causes')


def test_category(toolkit):
    assert toolkit.is_category('named thing')
    assert toolkit.is_category('gene')
    assert not toolkit.is_category('causes')
    assert not toolkit.is_category('affects')


def test_ancestors(toolkit):
    assert 'related to' in toolkit.get_ancestors('causes')
    assert 'biolink:related_to' in toolkit.get_ancestors('causes', formatted=True)

    assert 'named thing' in toolkit.get_ancestors('gene')
    assert 'biolink:NamedThing' in toolkit.get_ancestors('gene', formatted=True)

    assert 'causes' in toolkit.get_ancestors('causes')
    assert 'causes' in toolkit.get_ancestors('causes', reflexive=True)
    assert 'causes' not in toolkit.get_ancestors('causes', reflexive=False)
    assert 'biolink:causes' in toolkit.get_ancestors('causes', reflexive=True, formatted=True)

    assert 'drug exposure' in toolkit.get_ancestors('drug intake', reflexive=True)


def test_descendants(toolkit):
    assert 'causes' in toolkit.get_descendants('related to')
    assert 'interacts with' in toolkit.get_descendants('related to')
    assert 'gene' in toolkit.get_descendants('named thing')
    assert 'phenotypic feature' in toolkit.get_descendants('named thing')
    assert 'biolink:PhenotypicFeature' in toolkit.get_descendants('named thing', formatted=True)

    assert 'genomic entity' in toolkit.get_ancestors('genomic entity')
    assert 'genomic entity' in toolkit.get_ancestors('genomic entity', reflexive=True)
    assert 'genomic entity' not in toolkit.get_ancestors('genomic entity', reflexive=False)
    assert 'biolink:GenomicEntity' in toolkit.get_ancestors('gene', formatted=True)

    assert 'gross anatomical structure' in toolkit.get_ancestors('tissue', reflexive=True)
    assert 'molecular activity_has output' not in toolkit.get_descendants('molecular activity', reflexive=True)
    assert 'molecular activity_has output' not in toolkit.get_descendants('has output', reflexive=True)


def test_children(toolkit):
    assert 'causes' in toolkit.get_children('contributes to')
    assert 'physically interacts with' in toolkit.get_children('interacts with')
    assert 'gene' in toolkit.get_children('gene or gene product')
    assert 'biolink:Gene' in toolkit.get_children('gene or gene product', formatted=True)


def test_parent(toolkit):
    assert 'contributes to' in toolkit.get_parent('causes')
    assert 'interacts with' in toolkit.get_parent('physically interacts with')
    assert 'gene or gene product' in toolkit.get_parent('gene')
    assert 'biolink:GeneOrGeneProduct' in toolkit.get_parent('gene or gene product', formatted=True)


def test_mapping(toolkit):
    assert len(toolkit.get_all_elements_by_mapping('SO:0000704')) == 1
    assert 'gene' in toolkit.get_all_elements_by_mapping('SO:0000704')

    assert len(toolkit.get_all_elements_by_mapping('MONDO:0000001')) == 1
    assert 'disease' in toolkit.get_all_elements_by_mapping('MONDO:0000001')

    assert len(toolkit.get_all_elements_by_mapping('UPHENO:0000001')) == 1
    assert 'affects' in toolkit.get_all_elements_by_mapping('UPHENO:0000001')

    assert len(toolkit.get_all_elements_by_mapping('RO:0004033')) == 1
    assert 'negatively regulates' in toolkit.get_all_elements_by_mapping('RO:0004033')
    assert 'biolink:negatively_regulates' in toolkit.get_all_elements_by_mapping('RO:0004033', formatted=True)


def test_get_slot_domain(toolkit):
    assert 'treatment' in toolkit.get_slot_domain('treats')
    assert 'exposure event' in toolkit.get_slot_domain('treats', include_ancestors=True)
    assert 'biolink:ExposureEvent' in toolkit.get_slot_domain('treats', include_ancestors=True, formatted=True)

    assert 'biological process or activity' in toolkit.get_slot_domain('enabled by')
    assert 'biological entity' in toolkit.get_slot_domain('enabled by', include_ancestors=True)
    assert 'biolink:BiologicalEntity' in toolkit.get_slot_domain('enabled by', include_ancestors=True, formatted=True)

    assert 'entity' in toolkit.get_slot_domain('name')
    assert 'entity' in toolkit.get_slot_domain('category')
    assert 'association' in toolkit.get_slot_domain('relation')


def test_get_slot_range(toolkit):
    assert 'disease or phenotypic feature' in toolkit.get_slot_range('treats')
    assert 'biological entity' in toolkit.get_slot_range('treats', include_ancestors=True)
    assert 'biolink:BiologicalEntity' in toolkit.get_slot_range('treats', include_ancestors=True, formatted=True)

    assert 'label type' in toolkit.get_slot_range('name')
    assert 'uriorcurie' in toolkit.get_slot_range('relation')
    assert 'metatype:Uriorcurie' in toolkit.get_slot_range('relation', formatted=True)


def test_get_all_slots_with_class_domain(toolkit):
    assert 'treats' in toolkit.get_all_slots_with_class_domain('treatment')
    assert 'biolink:treats' in toolkit.get_all_slots_with_class_domain('treatment', formatted=True)


def test_get_all_slots_with_class_range(toolkit):
    assert 'treated by' in toolkit.get_all_slots_with_class_range('treatment')
    assert 'biolink:treated_by' in toolkit.get_all_slots_with_class_range('treatment', formatted=True)


def test_get_all_predicates_with_class_domain(toolkit):
    assert 'genetically interacts with' in toolkit.get_all_slots_with_class_domain('gene')
    assert 'interacts with' in toolkit.get_all_slots_with_class_domain('gene', check_ancestors=True)
    assert 'biolink:interacts_with' in toolkit.get_all_slots_with_class_domain('gene', check_ancestors=True, formatted=True)

    assert 'in complex with' in toolkit.get_all_slots_with_class_domain('gene or gene product')
    assert 'expressed in' in toolkit.get_all_slots_with_class_domain('gene or gene product')
    assert 'expressed in' in toolkit.get_all_slots_with_class_domain('gene or gene product')
    assert 'interacts with' in toolkit.get_all_slots_with_class_domain('gene or gene product', check_ancestors=True)
    assert 'biolink:interacts_with' in toolkit.get_all_slots_with_class_domain('gene or gene product', check_ancestors=True, formatted=True)


def test_get_all_predicates_with_class_range(toolkit):
    assert 'manifestation of' in toolkit.get_all_predicates_with_class_range('disease')
    assert 'disease has basis in' in toolkit.get_all_predicates_with_class_range('disease', check_ancestors=True)
    assert 'biolink:disease_has_basis_in' in toolkit.get_all_predicates_with_class_range('disease', check_ancestors=True, formatted=True)


def test_get_all_properties_with_class_domain(toolkit):
    assert 'category' in toolkit.get_all_properties_with_class_domain('entity')
    assert 'category' in toolkit.get_all_properties_with_class_domain('gene', check_ancestors=True)
    assert 'biolink:category' in toolkit.get_all_properties_with_class_domain('gene', check_ancestors=True, formatted=True)

    assert 'subject' in toolkit.get_all_properties_with_class_domain('association')
    assert 'subject' in toolkit.get_all_properties_with_class_domain('association', check_ancestors=True)
    assert 'biolink:subject' in toolkit.get_all_properties_with_class_domain('association', check_ancestors=True, formatted=True)


def test_get_all_properties_with_class_range(toolkit):
    assert 'has gene' in toolkit.get_all_properties_with_class_range('gene')
    assert 'subject' in toolkit.get_all_properties_with_class_range('gene', check_ancestors=True)
    assert 'biolink:subject' in toolkit.get_all_properties_with_class_range('gene', check_ancestors=True, formatted=True)


def test_get_value_type_for_slot(toolkit):
    assert 'uriorcurie' in toolkit.get_value_type_for_slot('subject')
    assert 'uriorcurie' in toolkit.get_value_type_for_slot('object')
    assert 'string' in toolkit.get_value_type_for_slot('symbol')
    assert 'biolink:CategoryType' in toolkit.get_value_type_for_slot('category', formatted=True)
