import DialogSkill from "../components/dialogSkill";

export default function UserSkills(){
    return (<>
        <div className="container-form">
            <DialogSkill isUpdate={true} isOpen={true}/>
        </div>
    </>)
}