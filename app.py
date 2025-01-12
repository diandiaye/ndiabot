import streamlit as st
import graphviz
from dataclasses import dataclass
from typing import Optional, Dict, List
import uuid

@dataclass
class FamilyMember:
    name: str
    role: str
    id: str
    photo_path: Optional[str] = None
    color: str = "lightgrey"
    parent_ids: List[str] = None

    def __init__(self, name, role, color="lightgrey", photo_path=None, parent_ids=None):
        self.name = name
        self.role = role
        self.id = str(uuid.uuid4())
        self.color = color
        self.photo_path = photo_path
        self.parent_ids = parent_ids if parent_ids else []

class FamilyTreeManager:
    def __init__(self):
        if 'families' not in st.session_state:
            st.session_state.families = self._initialize_families()

    def _create_base_family(self, family_name: str, color_scheme: Dict[str, str]) -> Dict[str, FamilyMember]:
        grandfather = FamilyMember(f"El Hadj {family_name}", "Grandfather", color=color_scheme['elder'])
        grandmother = FamilyMember(f"Adja {family_name}", "Grandmother", color=color_scheme['elder'])
        father = FamilyMember(f"Serigne {family_name}", "Father", color=color_scheme['parent'], 
                            parent_ids=[grandfather.id, grandmother.id])
        mother = FamilyMember(f"Sokhna {family_name}", "Mother", color=color_scheme['parent'])
        child1 = FamilyMember(f"Cheikh {family_name}", "Child", color=color_scheme['child'], 
                           parent_ids=[father.id, mother.id])
        child2 = FamilyMember(f"Aissatou {family_name}", "Child", color=color_scheme['child'], 
                           parent_ids=[father.id, mother.id])
        child3 = FamilyMember(f"Mamadou {family_name}", "Child", color=color_scheme['child'], 
                           parent_ids=[father.id, mother.id])
        
        # Adding grandchildren
        grandchild1 = FamilyMember(f"Fatou {family_name}", "Grandchild", color=color_scheme['grandchild'], 
                                   parent_ids=[child1.id])
        grandchild2 = FamilyMember(f"Ali {family_name}", "Grandchild", color=color_scheme['grandchild'], 
                                   parent_ids=[child1.id])
        grandchild3 = FamilyMember(f"Youssou {family_name}", "Grandchild", color=color_scheme['grandchild'], 
                                   parent_ids=[child2.id])
        grandchild4 = FamilyMember(f"Ndèye {family_name}", "Grandchild", color=color_scheme['grandchild'], 
                                   parent_ids=[child3.id])
        
        return {
            member.id: member for member in [grandfather, grandmother, father, mother, child1, child2, child3, 
                                              grandchild1, grandchild2, grandchild3, grandchild4]
        }

    def _initialize_families(self):
        families = {}
        color_schemes = {
            "Ndao": {'elder': '#1E88E5', 'parent': '#42A5F5', 'child': '#90CAF9', 'grandchild': '#BBDEFB'},
            "Ndiaye": {'elder': '#FF5722', 'parent': '#FF7043', 'child': '#FFAB91', 'grandchild': '#FFCCBC'},
            "DIA": {'elder': '#4CAF50', 'parent': '#66BB6A', 'child': '#81C784', 'grandchild': '#A5D6A7'},
            "WANE": {'elder': '#FBC02D', 'parent': '#FDD835', 'child': '#FFEB3B', 'grandchild': '#FFF59D'},
            "KANE": {'elder': '#1976D2', 'parent': '#2196F3', 'child': '#64B5F6', 'grandchild': '#BBDEFB'},
            "Mbacké": {'elder': '#8E24AA', 'parent': '#AB47BC', 'child': '#E1BEE7', 'grandchild': '#F1E6F2'},
            "Sy": {'elder': '#D32F2F', 'parent': '#E57373', 'child': '#EF9A9A', 'grandchild': '#FFCDD2'},
            "Tall": {'elder': '#C2185B', 'parent': '#D81B60', 'child': '#F06292', 'grandchild': '#F8BBD0'},
            "SOUGOUFARA": {'elder': '#7B1FA2', 'parent': '#9C27B0', 'child': '#BA68C8', 'grandchild': '#E1BEE7'},
            "Aidara": {'elder': '#0288D1', 'parent': '#03A9F4', 'child': '#4FC3F7', 'grandchild': '#B3E5FC'},
            "AGNE": {'elder': '#F57C00', 'parent': '#FF9800', 'child': '#FFB74D', 'grandchild': '#FFE0B2'},
        }
        
        for family_name, color_scheme in color_schemes.items():
            families[family_name] = self._create_base_family(family_name, color_scheme)
        
        return families

    def update_member(self, family_name: str, member_id: str, new_name: str):
        family = st.session_state.families[family_name]
        if member_id in family:
            family[member_id].name = new_name

def create_family_tree_app():
    st.set_page_config(page_title="Senegalese Family Trees", layout="wide")
    st.title("🌳 Senegalese Family Trees Visualization")
    
    manager = FamilyTreeManager()
    
    page = st.sidebar.selectbox("Select Page", ["Family Tree", "Empty Family Tree"])
    
    if page == "Family Tree":
        selected_family = st.selectbox(
            "Select a Family",
            list(st.session_state.families.keys()),
            index=0
        )
        
        graph = graphviz.Digraph()
        graph.attr(rankdir='TB', size="8,8")  # Increased size for better visibility
        
        members = st.session_state.families[selected_family]
        
        for id, member in members.items():
            label = f"""<<TABLE BORDER="0" CELLBORDER="1" CELLSPACING="0" CELLPADDING="5">
                       <TR><TD PORT="img" BGCOLOR="{member.color}">{"🖼️" if member.photo_path else "👤"}</TD></TR>
                       <TR><TD>{member.name}<BR/><i>{member.role}</i></TD></TR>
                       </TABLE>>"""
            graph.node(id, label, shape="none", style="rounded", fillcolor=member.color, color="black")
        
        for member in members.values():
            if member.parent_ids:
                for parent_id in member.parent_ids:
                    graph.edge(parent_id, member.id, dir="none", color="black")

        st.graphviz_chart(graph, use_container_width=True)
        
        with st.sidebar:
            st.header("🔍 Update Family Member")
            member_id = st.selectbox("Select Member to Update", list(members.keys()))
            new_name = st.text_input("New Name")
            
            if st.button("Update Member"):
                if new_name:
                    manager.update_member(selected_family, member_id, new_name)
                    st.success(f"✅ Updated member to {new_name}")
                else:
                    st.error("⚠️ Please enter a name for the family member")

    elif page == "Empty Family Tree":
        st.header("Coming soon!")

if __name__ == "__main__":
    create_family_tree_app()
